import FWCore.ParameterSet.Config as cms

# Reclusterizer options

from RecoLocalTracker.SiPhase2Reclusterizer.default_phase2TrackerReclusterizer_cfi import default_phase2TrackerReclusterizer

siPhase2Clusters = default_phase2TrackerReclusterizer.clone(
    src = "siPhase2ClustersUnrefined",
    handleBadStrips = True,
    maxBadStrips = 1
)