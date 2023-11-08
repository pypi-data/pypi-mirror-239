from datetime import datetime, timedelta
from enum import Enum
import os
import pathlib
import subprocess
import tempfile
from typing import List, Union  # , Iterable

# import numpy as np

from pyschism import dates
from pyschism.enums import Stratification
from pyschism.hotstart import Hotstart

# from pyschism.forcing import Tides, Hydrology
from pyschism.forcing.source_sink import SourceSink
from pyschism.forcing.nws.base import NWS
from pyschism.forcing.nws.nws2 import NWS2
from pyschism.forcing.nws.best_track import BestTrackForcing

# from pyschism.forcing.baroclinic import BaroclinicForcing
from pyschism.forcing.bctides import Bctides
from pyschism.makefile import MakefileDriver
from pyschism.mesh import Hgrid, Vgrid, Fgrid, gridgr3, prop
from pyschism.mesh.fgrid import ManningsN, DragCoefficient
from pyschism.param import Param
from pyschism.server.base import ServerConfig
from pyschism.stations import Stations


def raise_type_error(argname, obj, cls):
    raise TypeError(
        f"Argument {argname} must be of type {cls}, not " f"type {type(obj)}."
    )


class ModelForcings:
    def __init__(self, bctides=None, nws=None, source_sink=None, waves=None):
        self.bctides = bctides
        self.nws = nws
        self.source_sink = source_sink
        self.waves = waves

    def write(
        self,
        driver: "ModelDriver",
        output_directory,
        overwrite,
    ):

        if self.bctides is not None:
            self.bctides.write(
                output_directory,
                start_date=driver.param.opt.start_date,
                rnday=driver.param.core.rnday,
                overwrite=True,
            )

        if self.nws is not None:
            if isinstance(self.nws, NWS2):
                self.nws.write(
                    output_directory,
                    start_date=driver.param.opt.start_date,
                    end_date=driver.param.core.rnday,
                    overwrite=overwrite,
                    bbox=driver.config.hgrid.get_bbox(output_type="bbox"),
                    prc=True if driver.config.vgrid.is3D() is True else False,
                    rad=True if driver.config.vgrid.is3D() is True else False,
                )
            elif isinstance(self.nws, BestTrackForcing):
                self.nws.write(
                    output_directory,
                    overwrite=overwrite,
                )

        if self.source_sink is not None:
            self.source_sink.write(
                output_directory,
                driver.config.hgrid,
                start_date=driver.param.opt.start_date,
                end_date=driver.param.core.rnday,
                overwrite=overwrite,
            )

        if self.waves is not None:
            self.waves.write()

class Gr3FieldTypes(Enum):
    ALBEDO = gridgr3.Albedo
    DIFFMIN = gridgr3.Diffmin
    DIFFMAX = gridgr3.Diffmax
    WATERTYPE = gridgr3.Watertype
    WINDROT = gridgr3.Windrot
    ESTUARY = gridgr3.Estuary

    @classmethod
    def _missing_(cls, name):
        raise ValueError(f"{name} is not a valid {gridgr3.Gr3Field} type.")


class PropTypes(Enum):
    FLUXFLAG = prop.Fluxflag
    TVDFLAG = prop.Tvdflag


class ModelDriver:
    def __init__(
        self,
        config: "ModelConfig",
        dt: Union[float, timedelta],
        rnday: Union[float, timedelta],
        start_date: datetime = None,
        dramp: Union[float, timedelta] = None,
        drampbc: Union[float, timedelta] = None,
        dramp_ss: Union[float, timedelta] = None,
        drampwafo: Union[float, timedelta] = None,
        drampwind: Union[float, timedelta] = None,
        elev_ic=None,
        temp_ic=None,
        salt_ic=None,
        nspool: Union[int, timedelta] = None,
        ihfskip: int = None,
        nhot_write: Union[int, timedelta] = None,
        stations: Stations = None,
        hotstart: Union[Hotstart, "ModelDriver"] = None,
        server_config: ServerConfig = None,
        param_template=None,
        **surface_outputs,
    ):
        self.config = config
        self.param = Param()

        # set core parameters
        self.param.core.dt = dt
        self.param.core.rnday = rnday
        self.param.core.nspool = nspool if nspool is not None else self.param.core.rnday
        self.param.core.ihfskip = (
            ihfskip if ihfskip is not None else timedelta(days=self.param.core.rnday)
        )
        # if self.config.vgrid.is2D():
        #     self.param.core.ibc = Stratification.BAROTROPIC
        #     if self.config.forcings.baroclinic is not None:
        #         self.param.core.ibtp = 1
        # else:
        #     self.param.core.ibc = Stratification.BAROCLINIC
        self.param.core.ibc = self.config.stratification

        # TODO: must also set msc2/mdc2 here.

        # set opt
        self.param.opt.start_date = start_date
        self.param.opt.ics = 2 if self.config.hgrid.crs.is_geographic is True else 1
        self.param.opt.ncor = 1 if self.param.opt.ics == 2 else 0
        self.param.opt.dramp = dramp
        self.param.opt.drampbc = drampbc
        self.param.opt.dramp_ss = dramp_ss
        self.param.opt.drampwafo = drampwafo
        self.param.opt.drampwind = drampwind

        # set friction parameters
        self.param.opt.nchi = self.config.fgrid.nchi
        if self.config.fgrid.nchi == -1:
            self.param.opt.hmin_man = self.config.fgrid.hmin_man

        elif self.config.fgrid.nchi == 1:
            self.param.opt.dbz_min = self.config.fgrid.dbz_min
            self.param.opt.dbz_decay = self.config.fgrid.dbz_decay

        self.param.schout.nhot_write = (
            self.param.core.ihfskip if nhot_write is None else nhot_write
        )

        self.tmpdir = tempfile.TemporaryDirectory()
        self.outdir = pathlib.Path(self.tmpdir.name)

        self.stations = stations

        self.server_config = server_config

        self.hotstart = hotstart

        self.elev_ic = elev_ic

        # set flag_ic
        # flag_ic(1) = 1 !T
        self.temp_ic = temp_ic
        # flag_ic(2) = 1 !S
        self.salt_ic = salt_ic

        # TODO: init tracers (flag_ic[2:])

        if self.config.forcings.nws is not None:
            if isinstance(self.config.forcings.nws, NWS2):
                if self.config.forcings.nws.windrot is None:
                    self.config.forcings.nws.windrot = gridgr3.Windrot.default(
                        self.config.hgrid
                    )
            elif isinstance(self.config.forcings.nws, BestTrackForcing):
                # Writing the rotation file is still needed, but it's
                # not meaningful for BestTrackForcing
                self.config.forcings.nws.windrot = gridgr3.Windrot.default(
                    self.config.hgrid
                )
                self.param.opt.model_type_pahm = self.config.forcings.nws.model.value

            self.param.opt.wtiminc = self.param.core.dt
            self.param.opt.nws = self.config.forcings.nws.dtype.value

        if self.config.forcings.source_sink is not None:
            if self.elev_ic is None:
                if self.hotstart is None:
                    self.elev_ic = True

        # TODO: init template
        self.param_template = param_template

        for var in self.param.schout.surface_output_vars:
            val = surface_outputs.pop(var) if var in surface_outputs else None
            if val is not None:
                setattr(self.param.schout, var, val)

        if len(surface_outputs) > 0:
            raise TypeError(
                "ModelDriver() got an unexpected keyword arguments"
                f" {list(surface_outputs)}."
            )

    def run(
        self,
        output_directory: Union[str, os.PathLike] = None,
        overwrite=False,
        use_param_template=False,
    ):
        self.outdir = (
            pathlib.Path(output_directory)
            if output_directory is not None
            else self.outdir
        )
        self.write(
            self.outdir, overwrite=overwrite, use_param_template=use_param_template
        )
        # Make sure we are using a fresh fatal.error file since we can't catch
        # blowup from mpiexec exit codes.
        error_file = self.outdir / "outputs/fatal.error"
        if error_file.exists() and overwrite is not True:
            raise IOError("File exists and overwrite is not True.")
        if error_file.exists() and overwrite is True:
            error_file.unlink()
        subprocess.check_call(["make", "run"], cwd=self.outdir)
        with open(error_file) as f:
            error = f.read()
        if "ABORT" in error:
            raise Exception(f"SCHISM exited with error:\n{error}")

    @property
    def config(self) -> "ModelConfig":
        return self._config

    @config.setter
    def config(self, config: "ModelConfig"):
        if not isinstance(config, ModelConfig):
            raise_type_error("config", config, ModelConfig)
        self._config = config

    @property
    def hotstart(self):
        return self._hotstart

    @hotstart.setter
    def hotstart(self, hotstart: Union[Hotstart, "ModelDriver", None]):

        if hotstart is None:
            pass

        else:
            if not isinstance(hotstart, Hotstart):
                if isinstance(hotstart, self.__class__):
                    hotstart = Hotstart.combine(hotstart.outdir / "outputs")
                else:
                    raise TypeError(
                        f"Argument hotstart must be of type {Hotstart}, "
                        f"{self.__class__} or None, not type {type(hotstart)}."
                    )

        if hotstart is not None:
            self.param.opt.ihot = 1

        self._hotstart = hotstart

    @property
    def stations(self) -> Stations:
        return self._stations

    @stations.setter
    def stations(self, stations: Union[Stations, None]):
        if stations is not None:
            if not isinstance(stations, Stations):
                raise_type_error("stations", stations, Stations)
        self._stations = stations

    def write(
        self,
        output_directory,
        overwrite=False,
        hgrid=True,
        vgrid=True,
        fgrid=True,
        param=True,
        bctides=True,
        nws=True,
        stations=True,
        use_param_template=False,
        albedo=True,
        diffmax=True,
        diffmin=True,
        watertype=True,
        windrot=True,
        shapiro=True,
        fluxflag=False,
        tvdflag=True,
        elev_ic=True,
        temp_ic=True,
        salt_ic=True,
        # rtofs=True,
        hydrology=True,
    ):
        """Writes to disk the full set of input files necessary to run SCHISM."""

        self.outdir = (
            pathlib.Path(output_directory)
            if output_directory is not None
            else self.outdir
        )

        if not (self.outdir / "outputs").exists():
            (self.outdir / "outputs").mkdir(parents=True, exist_ok=overwrite)

        if hgrid is not False:
            hgrid = "hgrid.gr3" if hgrid is True else hgrid
            self.config.hgrid.write(self.outdir / hgrid, overwrite)
            if self.param.opt.ics == 2:
                _original_dir = os.getcwd()
                os.chdir(self.outdir)  # pushd
                try:
                    os.remove("hgrid.ll")
                except OSError:
                    pass
                os.symlink(hgrid, "hgrid.ll")
                os.chdir(_original_dir)  # popd

        if vgrid is not False:
            vgrid = "vgrid.in" if vgrid is True else vgrid
            self.config.vgrid.write(self.outdir / vgrid, overwrite)

        if fgrid is not False:
            fgrid = f"{self.config.fgrid.fname}" if fgrid is True else fgrid
            self.config.fgrid.write(self.outdir / fgrid, overwrite)

        if param is not False:
            param = "param.nml" if param is True else param
            self.param.write(
                self.outdir / param, overwrite, use_template=use_param_template
            )

        def obj_write(var, obj, default_filename, overwrite):
            if var is not False and obj is not None:
                obj.write(
                    self.outdir / default_filename if var is True else var, overwrite
                )

        obj_write(albedo, self.config.albedo, "albedo.gr3", overwrite)
        obj_write(diffmin, self.config.diffmin, "diffmin.gr3", overwrite)
        obj_write(diffmax, self.config.diffmax, "diffmax.gr3", overwrite)
        obj_write(watertype, self.config.watertype, "watertype.gr3", overwrite)
        obj_write(windrot, self.config.windrot, "windrot_geo2proj.gr3", overwrite)
        obj_write(shapiro, self.config.shapiro, "shapiro.gr3", overwrite)
        obj_write(fluxflag, self.config.fluxflag, "fluxflag.prop", overwrite)
        obj_write(tvdflag, self.config.tvdflag, "tvd.prop", overwrite)
        obj_write(temp_ic, self.temp_ic, "temp.ic", overwrite)
        obj_write(salt_ic, self.salt_ic, "salt.ic", overwrite)
        obj_write(elev_ic, self.elev_ic, "elev.ic", overwrite)
        obj_write(stations, self.stations, "station.in", overwrite)

        self.config.forcings.write(
            self, output_directory, overwrite,
        )

        MakefileDriver(self.server_config, hotstart=self.hotstart).write(
            self.outdir / "Makefile", overwrite
        )

    @property
    def outdir(self):
        return self._outdir

    @outdir.setter
    def outdir(self, outdir):
        self.config.outdir = outdir
        self._outdir = outdir

    @property
    def elev_ic(self):
        return self._elev_ic

    @elev_ic.setter
    def elev_ic(self, elev_ic: Union[None, bool, gridgr3.ElevIc]):
        if elev_ic is not None:
            if not isinstance(elev_ic, (gridgr3.ElevIc, bool)):
                raise_type_error("elev_ic", elev_ic, gridgr3.ElevIc)
            if elev_ic is True:
                elev_ic = gridgr3.ElevIc.default(self.config.hgrid)
            self.param.opt.ic_elev = 1
            if elev_ic is False:
                self.param.opt.ic_elev = 0
        self._elev_ic = elev_ic

    @elev_ic.deleter
    def elev_ic(self):
        self.param.opt.ic_elev = None
        self._elev_ic = None


class Gridgr3Descriptor:
    def __init__(self, gridgr3_type: Gr3FieldTypes):
        self.name = gridgr3_type.name
        self.type = gridgr3_type.value
        self.gr3field = None

    def __set__(self, obj, val: Union[gridgr3.Gr3Field, None]):
        if not isinstance(val, self.type) and val is not None:
            raise ValueError(
                f"Argument {self.name.lower()} must be of type {self.type} "
                f"not type {type(val)}."
            )
        self.gr3field = val

    def __get__(self, obj, val):
        return self.gr3field


class PropTypeDescriptor:
    def __init__(self, prop_type: PropTypes):
        self.name = prop_type.name
        self.type = prop_type.value
        self.prop = None

    def __set__(self, obj, val: Union[prop.Prop, None]):
        if not isinstance(val, self.type) and val is not None:
            raise ValueError(
                f"Argument {self.name.lower()} must be of type {self.type} "
                f"not type {type(val)}."
            )
        self.prop = val

    def __get__(self, obj, val):
        return self.prop


class ModelConfigMeta(type):
    def __new__(meta, name, bases, attrs):
        # attrs['forcings'] = ModelForcings()
        attrs["start_date"] = dates.StartDate()
        attrs["end_date"] = dates.EndDate()
        attrs["spinup_time"] = dates.SpinupTime()
        for gr3field_type in Gr3FieldTypes:
            name = gr3field_type.name.lower()
            attrs[name] = Gridgr3Descriptor(gr3field_type)
        for prop_type in PropTypes:
            name = prop_type.name.lower()
            attrs[name] = PropTypeDescriptor(prop_type)
        return type(name, bases, attrs)


class ModelConfig(metaclass=ModelConfigMeta):
    """Class representing a SCHISM model configuration.

    This class combines the horizontal grid (hgrid), vertical grid (vgrid)
    and friction/drag grids (fgrid). Additionally, this class holds
    information about forcings.

    Args:
        hgrid: :class:`pyschism.mesh.Hgrid` instance.
        vgrid: :class:`pyschism.mesh.Vgrid` instance.
        fgrid: :class:`pyschism.mesh.Fgrid` derived instance.
    """

    def __init__(
        self,
        hgrid: Hgrid,
        vgrid: Vgrid = None,
        fgrid: Fgrid = None,
        flags = None,
        constituents = 'major',
        database = 'tpxo',
        add_earth_tidal = True,
        ethconst = None,
        vthconst = None,
        tthconst = None,
        sthconst = None,
        tobc = None,
        sobc = None,
        relax = None, 
        # itrtype: itrtype.Itrtype = None,
        nws: NWS = None,
        source_sink: Union[List[SourceSink], SourceSink] = None,
        waves=None,
        stratification: Union[int, str, Stratification] = None,
        albedo: gridgr3.Albedo = None,
        diffmin: gridgr3.Diffmin = None,
        diffmax: gridgr3.Diffmax = None,
        watertype: gridgr3.Watertype = None,
        estuary: gridgr3.Estuary = None,
        shapiro: gridgr3.Shapiro = None,
        fluxflag: prop.Fluxflag = None,
        tvdflag: prop.Tvdflag = None,
    ):
        self.hgrid = hgrid
        self.vgrid = vgrid
        self.fgrid = fgrid
        self.flags = flags
        self.constituents = constituents
        self.add_earth_tidal = add_earth_tidal
        self.ethconst = ethconst
        self.vthconst = vthconst
        self.tthconst = tthconst
        self.sthconst = sthconst
        self.tobc = tobc
        self.sobc = sobc
        self.relax = relax
        # self.itrtype = itrtype
        self.nws = nws
        self.source_sink = source_sink
        self.waves = waves
        self.stratification = stratification
        self.albedo = albedo
        self.diffmin = diffmin
        self.diffmax = diffmax
        self.watertype = watertype
        self.shapiro = shapiro
        self.fluxflag = fluxflag
        self.tvdflag = tvdflag
        self.estuary = estuary

    def coldstart(
        self,
        timestep: Union[float, timedelta] = 150.0,
        start_date: datetime = None,
        end_date: Union[datetime, timedelta] = None,
        dramp: Union[float, timedelta] = None,
        drampbc: Union[float, timedelta] = None,
        dramp_ss: Union[float, timedelta] = None,
        drampwafo: Union[float, timedelta] = None,
        drampwind: Union[float, timedelta] = None,
        elev_ic: gridgr3.ElevIc = None,
        temp_ic: gridgr3.TempIc = None,
        salt_ic: gridgr3.TempIc = None,
        nspool: Union[int, timedelta] = None,
        ihfskip: int = None,
        nhot_write: Union[int, timedelta] = None,
        stations: Stations = None,
        server_config: ServerConfig = None,
        param_template=None,
        **surface_outputs,
    ) -> ModelDriver:

        if start_date is None:
            start_date = dates.nearest_cycle()

        if not isinstance(start_date, datetime):
            raise TypeError(
                f"Argument start_date must be of type {datetime} "
                f"or None, not type {type(start_date)}."
            )

        if end_date is None:
            end_date = self.forcings.maximum_end_date()

        if isinstance(end_date, timedelta):
            end_date = start_date + end_date

        if isinstance(end_date, (int, float)):
            end_date = start_date + timedelta(days=float(end_date))

        if not isinstance(end_date, datetime):
            raise TypeError(
                f"Argument end_date must be of type {datetime}, {timedelta}, "
                f"or None, not type {type(end_date)}."
            )

        return ModelDriver(
            self,
            dt=timestep,
            start_date=start_date,
            rnday=end_date - start_date,
            dramp=dramp,
            drampbc=drampbc,
            dramp_ss=dramp_ss,
            drampwafo=drampwafo,
            drampwind=drampwind,
            elev_ic=elev_ic,
            temp_ic=temp_ic,
            salt_ic=salt_ic,
            stations=stations,
            nspool=nspool,
            nhot_write=nhot_write,
            server_config=server_config,
            ihfskip=ihfskip,
            param_template=param_template,
            **surface_outputs,
        )

    def hotstart(
        self,
        hotstart: Union[Hotstart, ModelDriver],
        timestep: Union[float, timedelta] = 150.0,
        end_date: Union[datetime, timedelta] = None,
        nspool: Union[int, timedelta] = None,
        ihfskip: int = None,
        nhot_write: Union[int, timedelta] = None,
        stations: Stations = None,
        server_config: ServerConfig = None,
        **surface_outputs,
    ) -> ModelDriver:

        if isinstance(hotstart, ModelDriver):
            hotstart = Hotstart.combine(pathlib.Path(hotstart.outdir) / "outputs")

        if not isinstance(hotstart, Hotstart):
            raise TypeError(
                f"Argument hotstart must be of type {Hotstart}, "
                f"not type {type(hotstart)}."
            )

        if end_date is None:
            end_date = self.forcings.max_end_date()
            if end_date is None:
                raise ValueError("end_date is unbounded, must pass end_date argument.")
        if not isinstance(end_date, datetime):
            if isinstance(end_date, timedelta):
                end_date = hotstart.time + end_date
            else:
                end_date = hotstart.time + timedelta(days=float(end_date))

        return ModelDriver(
            self,
            dt=timestep,
            start_date=hotstart.time,
            rnday=end_date - hotstart.time,
            hotstart=hotstart,
            nspool=nspool,
            ihfskip=ihfskip,
            stations=stations,
            nhot_write=nhot_write,
            server_config=server_config,
            elev_ic=None,
            temp_ic=None,
            salt_ic=None,
            **surface_outputs,
        )

    @property
    def hgrid(self):
        return self._hgrid

    @hgrid.setter
    def hgrid(self, hgrid: Hgrid):
        if not isinstance(hgrid, Hgrid):
            raise_type_error("hgrid", hgrid, Hgrid)
        self._hgrid = hgrid

    @property
    def vgrid(self):
        return self._vgrid

    @vgrid.setter
    def vgrid(self, vgrid: Union[Vgrid, None]):
        if vgrid is None:
            vgrid = Vgrid.default()
        if not isinstance(vgrid, Vgrid):
            raise_type_error("vgrid", vgrid, Vgrid)
        self._vgrid = vgrid

    @property
    def fgrid(self):
        return self._fgrid

    @fgrid.setter
    def fgrid(self, fgrid: Union[Fgrid, None]):
        if fgrid is None:
            if self.vgrid.is2D():
                fgrid = ManningsN.linear_with_depth(self.hgrid)
            else:
                fgrid = DragCoefficient.linear_with_depth(self.hgrid)

        if not isinstance(fgrid, Fgrid):
            raise_type_error("fgrid", fgrid, Fgrid)

        if self.vgrid.is2D() is True and not isinstance(fgrid, ManningsN):
            raise TypeError(f"2D model must use {ManningsN} but got {type(fgrid)}.")

        self._fgrid = fgrid

    @property
    def timestep(self):
        return self._timestep

    @timestep.setter
    def timestep(self, timestep: Union[float, timedelta, None]):
        if timestep is None:
            self._timestep = timedelta(seconds=150.0)
        elif not isinstance(timestep, timedelta):
            self._timestep = timedelta(seconds=float(timestep))
        return self._timestep

    @property
    def outdir(self):
        return self._outdir

    @outdir.setter
    def outdir(self, outdir):
        self._outdir = pathlib.Path(outdir)

    @property
    def stratification(self):
        return self._stratification

    @stratification.setter
    def stratification(self, stratification: Union[str, Stratification, int, None]):
        if not isinstance(stratification, (str, Stratification, type(None))):
            raise TypeError(
                f"Argument stratification must be a str, {Stratification}, int (0 or 1), or None, not "
                f"type {type(stratification)}."
            )
        if stratification is None:
            if self.vgrid.is2D() is True:
                stratification = Stratification.BAROTROPIC
            else:
                stratification = Stratification.BAROCLINIC
        elif isinstance(stratification, (str, int)):
            stratification = Stratification(stratification)
        self._stratification = stratification

    @property
    def forcings(self):
        if not hasattr(self, "_forcings"):
            self._forcings = ModelForcings(
                bctides=self.bctides,
                nws=self.nws,
                source_sink=self.source_sink,
                waves=self.waves,
            )

        return self._forcings

    @property
    def bctides(self):
        if not hasattr(self, "_bctides"):
            self._bctides = Bctides(
                hgrid = self.hgrid,
                flags = self.flags,
                constituents = self.constituents,
                add_earth_tidal = self.add_earth_tidal,
                ethconst = self.ethconst,
                vthconst = self.vthconst,
                tthconst = self.tthconst,
                sthconst = self.sthconst,
                tobc = self.tobc,
                sobc = self.sobc,
                relax = self.relax,
                # cutoff_depth=self.cutoff_depth,
            )
        return self._bctides
