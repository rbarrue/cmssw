# Imports
import FWCore.ParameterSet.Config as cms

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
    input = cms.untracked.int32(200)
)

# Input file
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_15_1_0/RelValTTbar_14TeV/GEN-SIM-RECO/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D110_noPU-v1/2590000/002a6949-6471-46fd-8c44-1f09e7717c8f.root', \
        '/store/relval/CMSSW_15_1_0/RelValTTbar_14TeV/GEN-SIM-RECO/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D110_noPU-v1/2590000/0e60c3b1-0c21-41d2-94de-435382ae2b44.root')
    )

# Output
process.TFileService = cms.Service('TFileService',
    fileName = cms.string('file:cluster_validation.root')
)

# DEBUG
#process.MessageLogger = cms.Service('MessageLogger',
#	debugModules = cms.untracked.vstring('siPhase2Clusters'),
#	destinations = cms.untracked.vstring('cout'),
#	cout = cms.untracked.PSet(
#		threshold = cms.untracked.string('ERROR')
#	)
#)

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
process.p = cms.Path(process.analysis)
