# Imports
import FWCore.ParameterSet.Config as cms

# Create a new CMS process
process = cms.Process('hittree')

# Import all the necessary files
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.Geometry.GeometryExtendedRun4D110Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T33', '')


# Number of events (-1 = all)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(25)
    #input = cms.untracked.int32(100)
)

# Input file
# dataset: /RelValTTbar_14TeV/CMSSW_15_1_0-150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D110_noPU-v1/GEN-SIM-RECO
process.source = cms.Source('PoolSource',

    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_15_1_0/RelValTTbar_14TeV/GEN-SIM-RECO/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D110_noPU-v1/2590000/002a6949-6471-46fd-8c44-1f09e7717c8f.root', \
        '/store/relval/CMSSW_15_1_0/RelValTTbar_14TeV/GEN-SIM-RECO/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D110_noPU-v1/2590000/0e60c3b1-0c21-41d2-94de-435382ae2b44.root')
)

# Output
process.TFileService = cms.Service('TFileService',
    fileName = cms.string('file:rechits_tree_tt_with_reclusters.root')
)

process.load('RecoLocalTracker.SiPhase2Clusterizer.phase2TrackerClusterizer_cfi')
process.siPhase2ClustersUnrefined.maxClusterSize = 8
process.load('RecoLocalTracker.SiPhase2Reclusterizer.phase2TrackerReclusterizer_cfi')
process.load('RecoLocalTracker.Phase2TrackerRecHits.Phase2StripCPEESProducer_cfi')
#process.load('RecoLocalTracker.Phase2TrackerRecHits.Phase2StripCPEGeometricESProducer_cfi')
process.load('RecoLocalTracker.Phase2TrackerRecHits.Phase2TrackerRecHits_cfi')
#process.siPhase2RecHits.Phase2StripCPE = cms.ESInputTag("phase2StripCPEESProducer", "Phase2StripCPE")
#process.siPhase2RecHits.Phase2StripCPE = cms.ESInputTag("phase2StripCPEGeometricESProducer", "Phase2StripCPEGeometric")


# Analyzer
process.analysis = cms.EDAnalyzer('RecHitTreeWA',
    rechits = cms.InputTag("siPhase2RecHits"),
    clusters = cms.InputTag("siPhase2Clusters"),
    links = cms.InputTag("simSiPixelDigis", "Tracker"),
    simhitsbarrel = cms.InputTag("g4SimHits", "TrackerHitsPixelBarrelLowTof"),
    simhitsendcap = cms.InputTag("g4SimHits", "TrackerHitsPixelEndcapLowTof"),
    simtracks = cms.InputTag("g4SimHits"),
    #ECasRings = cms.bool(True),
    SimTrackMinPt = cms.double(0.5),
    #MakeEtaPlots = cms.bool(False),
    #MinEta = cms.double(0.),
    #MaxEta = cms.double(10.)
    debugHitMatch = cms.bool(False)
)

# Processes to run
process.cluster_step = cms.Path(process.siPhase2ClustersUnrefined + process.siPhase2Clusters)
#process.rechits_step = cms.Path(process.siPhase2Clusters + process.siPhase2RecHits)
process.rechits_step = cms.Path(process.siPhase2RecHits)
process.analyze_step = cms.Path(process.analysis)

process.schedule = cms.Schedule(process.cluster_step, process.rechits_step, process.analyze_step)


