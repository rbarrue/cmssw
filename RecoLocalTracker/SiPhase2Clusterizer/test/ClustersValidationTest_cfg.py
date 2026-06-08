# Imports
import FWCore.ParameterSet.Config as cms
import os

# Create a new CMS process
process = cms.Process('cluTest')

# Import all the necessary files
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
#process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtendedRun4D110Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T33', '')


# Number of events (-1 = all)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

# Input file
process.source = cms.Source('PoolSource',
    # 10 GeV Muon from RelVal of CMSSW 15.1
    fileNames = cms.untracked.vstring('/store/relval/CMSSW_15_1_0/RelValTTbar_14TeV/GEN-SIM-RECO/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D110_noPU-v1/2590000/002a6949-6471-46fd-8c44-1f09e7717c8f.root')
)

# Output
process.TFileService = cms.Service('TFileService',
    fileName = cms.string(f'file:{os.path.basename(__file__)}/cluster_validation.root')
)

# DEBUG
#process.MessageLogger = cms.Service('MessageLogger',
#	debugModules = cms.untracked.vstring('siPhase2Clusters'),
#	destinations = cms.untracked.vstring('cout'),
#	cout = cms.untracked.PSet(
#		threshold = cms.untracked.string('ERROR')
#	)
#)

process.load('RecoLocalTracker.SiPhase2Clusterizer.phase2TrackerClusterizer_cfi')
# fake strip source with all the strips killed for testing
# loaded via the Geometry files
process.SiPhase2OTFakeBadStripsESSource.badComponentsFraction = 0.05
# flag to handle bad strips
process.siPhase2Clusters.handleBadStrips = True

# redoing clustering to check access to bad strips
process.cluster_step = cms.Path(process.siPhase2Clusters)

# Analyzer
process.analysis = cms.EDAnalyzer('Phase2TrackerClusterizerValidation',
    src = cms.InputTag("siPhase2Clusters"),
    links = cms.InputTag("simSiPixelDigis", "Tracker"),
    simhitsbarrel = cms.InputTag("g4SimHits", "TrackerHitsPixelBarrelLowTof"),
    simhitsendcap = cms.InputTag("g4SimHits", "TrackerHitsPixelEndcapLowTof"),
    simtracks = cms.InputTag("g4SimHits"),
    ECasRings = cms.bool(True),
    SimTrackMinPt = cms.double(2.)
)

# Processes to run
process.analysis_step = cms.Path(process.analysis)
process.schedule = cms.Schedule(process.cluster_step, process.analysis_step) 
