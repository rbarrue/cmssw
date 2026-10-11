# Imports
import FWCore.ParameterSet.Config as cms

# Create a new CMS process
process = cms.Process('clusterMergerValidation')

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
    input = cms.untracked.int32(100)
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
    fileName = cms.string('file:clustermerger_validation.root')
)

process.load('RecoLocalTracker.SiPhase2Clusterizer.phase2TrackerClusterizer_cfi')
process.siPhase2Clusters.maxClusterSize = 8
process.load('RecoLocalTracker.SiPhase2Clusterizer.phase2TrackerClusterMerger_cfi')
# fake strip source loaded via the Geometry files
process.SiPhase2OTFakeBadStripsESSource.badComponentsFraction = 0.05
# flag to handle bad strips
process.siPhase2ClustersMerged.handleBadStrips = True
process.siPhase2ClustersMerged.maxBadStrips = 1

process.analysis = cms.EDAnalyzer('Phase2TrackerClusterizerValidation',
    src = cms.InputTag("siPhase2ClustersMerged"),
    links = cms.InputTag("simSiPixelDigis", "Tracker"),
    simhitsbarrel = cms.InputTag("g4SimHits", "TrackerHitsPixelBarrelLowTof"),
    simhitsendcap = cms.InputTag("g4SimHits", "TrackerHitsPixelEndcapLowTof"),
    simtracks = cms.InputTag("g4SimHits"),
    ECasRings = cms.bool(True),
    SimTrackMinPt = cms.double(2.)
)

process.analysisReco = process.analysis.clone(src = cms.InputTag("siPhase2Clusters","","RECO"))

# Processes to run
process.cluster_step = cms.Path(process.siPhase2Clusters+process.siPhase2ClustersMerged)
process.analyze_step = cms.Path(process.analysis+process.analysisReco)

process.schedule = cms.Schedule(process.cluster_step, process.analyze_step) 
