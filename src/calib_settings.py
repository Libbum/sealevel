import numpy as np
import get_calibration_data as gd; reload(gd)
import collections

""" calibration setting for each component.
    Provides the available observations for each component,
    The observation period for each component (and each observation)
    is the period that is taken for the calibration of the model.
    If observation period is None, full period of observation is taken.
    The temp anomaly year is when the GMT first kicks in to drive the
    sea-level parametrization. If None, the full GMT period is taken
    to drive the parametrization.
"""

observation_period = {}
temp_anomaly_year = {}

######## Thermal expansion ########

## Most thermal expansion observations are from 0-700m. We produce all
## combinations of these with the available observations below 700m.
## Each of these constructed "full depth" observations is used for
## the calibration of the model with each of the commitment factors
## for thermal expansion.

## dummy assuming no trend
zero = gd.church_observed_700m_2000m.copy()
zero[:] = 0.

contrib_upper700 = collections.OrderedDict([
("domingues08",gd.thermo_obs_domingues08),
("ishii09",gd.thermo_obs_ishii09),
("levitus12",gd.thermo_obs_levit12_700),
# ("church11",gd.church_observed_700m)]
])

contrib_700_2000m = collections.OrderedDict([
("levitus12",gd.thermo_obs_levit12_2000 - gd.thermo_obs_levit12_700),
("church11",gd.church_observed_700m_2000m)])

contrib_below2000m = collections.OrderedDict([
("zero",zero),
("purkey10",gd.purkey10_below2000m)])

def remix_therm_observations(above700m,between700_2000m,below2000m):

    """ find all combinations for thermosteric observations. """

    obs = collections.OrderedDict()
    for ab700 in above700m:
        for bet700_2000 in between700_2000m:
            for bel2000 in below2000m:
                lbl = ab700+"_"+bet700_2000+"_"+bel2000
                obs[lbl] = above700m[ab700] + between700_2000m[bet700_2000] + below2000m[bel2000]
                obs[lbl] = obs[lbl].dropna()
                # print lbl,obs[lbl].values
    return obs

thermexp_observations = remix_therm_observations(contrib_upper700,contrib_700_2000m,contrib_below2000m)

# the same observational period and anomaly year for all datasets.
observation_period["thermexp"] = {}
temp_anomaly_year["thermexp"] = {}
for obs in thermexp_observations:
    observation_period["thermexp"][obs] = None#np.arange(1970,2013,1)
    temp_anomaly_year["thermexp"][obs] = None
    if "domingues08" in obs:
        observation_period["thermexp"][obs] = np.arange(1970,2013,1)


######## Glaciers and icecaps ########

gic_observations = collections.OrderedDict([
("leclerqu11",gd.glacier_obs_leclercq11),
("cogley09",gd.glacier_obs_cogley09),
("marzeion12",gd.glacier_obs_marzeion12)])

# the same observational period and anomaly year for all datasets.
observation_period["gic"] = {}
temp_anomaly_year["gic"] = {}
for obs in gic_observations:
    observation_period["gic"][obs] = np.arange(1930,2013,1)
    temp_anomaly_year["gic"][obs] = None


######## Greenland surface mass balance ########

gis_smb_observations = collections.OrderedDict([
    ("church11",gd.church_gis_smb),
    ("angelen14",gd.angelen14),
    ("box_colgan13",gd.box_gis_smb),
])

op = np.arange(1960,2014,1)
observation_period["gis_smb"] = {"box_colgan13":None,"church11":None,"angelen14":None}
## Note: anomaly year should never be set later than first year of observations, otherwise
##       the "zero or negative" before anomaly year is included for calibration which is bad.
temp_anomaly_year["gis_smb"] = {"box_colgan13":None,"church11":None,"angelen14":None}


######## Greenland solid ice discharge ########

gis_sid_observations = collections.OrderedDict([
    ("sasgen12",gd.sasgen_sid),
    ("church11",gd.church_gis_sid),
    ("box_colgan13",gd.marine_ice_loss(gd.box_gis_smb)),
    ])

op = np.arange(1970,2009,1)
observation_period["gis_sid"] = {"box_colgan13":None,"church11":op,"sasgen12":np.arange(1992,2013,1)}
temp_anomaly_year["gis_sid"] = {"box_colgan13":None,"church11":1961,"sasgen12":1961}


######## Antarctica solid ice discharge ########

# no observed SMB trend in Antarctica until now, so assume all Church et al. observed change is SID
ant_sid_observations = collections.OrderedDict([
("church11",gd.church_observed["ant"]),
("mouginot_rignot14",gd.mouginot_ase_sl),
("harig_simons15",gd.harig_simons15),
])

op = np.arange(1960,2009,1)
observation_period["ant_sid"] = {"church11":op,"mouginot_rignot14":op,"harig_simons15":op}
temp_anomaly_year["ant_sid"] = {"church11":None,"mouginot_rignot14":1980,"harig_simons15":1980}


######## Antarctica surface mass balance ########

## these are dummies and not used, just to avoid "if code" in routines.

ant_smb_observations = collections.OrderedDict([("ligtenberg13","dummy")])
observation_period["ant_smb"] = {"ligtenberg13":np.arange(1970,2009,1)}
temp_anomaly_year["ant_smb"] = {"ligtenberg13":None}


# ## models are calibrated over the observation period.
# observation_period = {
# "thermexp":np.arange(1970,2009,1),
# # "gic":np.arange(1940,2014,1),
# "gic":np.arange(1940,2014,1),
# # "gis":np.arange(1960,2009,1),
# "gis_smb":np.arange(1960,2009,1),
# "gis_sid":np.arange(1970,2009,1),
# "ant_sid":np.arange(1960,2009,1),
# "ant_smb":np.arange(1970,2009,1) # this is fake for plotting
# }

# ## temp anomaly year is when GMT first kicks in to drive SL of parametrization.
# ## if None, full GMT period is taken
# temp_anomaly_year = {
# "thermexp":None,
# "gic":None,
# "gis_smb":None,
# "gis_sid":1961,
# "ant_sid":1990,
# "ant_smb":None,
# }

