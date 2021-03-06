#------------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------------
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
import FWCore.ParameterSet.VarParsing as VarParsing

#------------------------------------------------------------------------------------
# Options
#------------------------------------------------------------------------------------
options = VarParsing.VarParsing()

options.register('skipEvents',
                 0, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to skip")

options.register('processEvents',
#                 -1, # default value
                  20,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to process")

options.register('inputFiles',
#                 "root://cmsxrootd.fnal.gov//store/express/Commissioning2017/ExpressPhysics/FEVT/Express-v1/000/293/591/00000/F45D88B0-A234-E711-B36A-02163E01A6B2.root", # default value
#                 "/store/data/Run2018A/IsolatedBunch/RAW/v1/000/316/615/00000/E08341F0-4364-E811-B866-FA163EC65D0D.root",
#                 "/store/data/Run2018B/IsolatedBunch/RAW/v1/000/317/279/00000/F8E4C1C9-1A65-E811-BA53-FA163EED2759.root",
#                  "/store/data/Run2018A/MinimumBias/RAW/v1/000/315/557/00000/66948AB0-144E-E811-84CC-FA163EC307AB.root",
                   "/store/data/Run2018A/JetHT/RAW/v1/000/316/722/00000/DE166863-8C64-E811-8221-FA163ECE1721.root ",
#                  "/store/data/Run2018B/JetHT/RAW-RECO/JetHTJetPlusHOFilter-PromptReco-v1/000/317/279/00000/F6FD04FA-D466-E811-A905-FA163E7A1DE1.root",
                 VarParsing.VarParsing.multiplicity.list,
                 VarParsing.VarParsing.varType.string,
                 "Input files")

options.register('outputFile',
#                 "HcalTupleMaker.root", # default value
                 "results.root", # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Output file")

options.parseArguments()

print " "
print "Using options:"
print " skipEvents    =", options.skipEvents
print " processEvents =", options.processEvents
print " inputFiles    =", options.inputFiles
print " outputFile    =", options.outputFile
print " "

#------------------------------------------------------------------------------------
# Declare the process and input variables
#------------------------------------------------------------------------------------
process = cms.Process('PFG',eras.Run2_2018)

#------------------------------------------------------------------------------------
# Get and parse the command line arguments
#------------------------------------------------------------------------------------
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.processEvents) )

process.source = cms.Source(
    "PoolSource",
    fileNames  = cms.untracked.vstring(options.inputFiles),
#    secondaryFileNames = cms.untracked.vstring(
#    "/store/data/Run2018B/JetHT/RAW/v1/000/317/279/00000/8881327C-1165-E811-B99D-FA163E8F269A.root",
#    "/store/data/Run2018B/JetHT/RAW/v1/000/317/279/00000/6CC9E44D-1165-E811-9A70-FA163E60A5FD.root"
#    ""
#    ),
    skipEvents = cms.untracked.uint32(options.skipEvents)
    )

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
    )

#------------------------------------------------------------------------------------
# import of standard configurations
#------------------------------------------------------------------------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('RecoMET.METProducers.hcalnoiseinfoproducer_cfi')
process.load("CommonTools.RecoAlgos.HBHENoiseFilter_cfi")
process.load("CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi")
process.load("CondCore.CondDB.CondDB_cfi")
#process.load('RecoLocalCalo.Configuration.RecoLocalCalo_Cosmics_cff')
process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")
#process.load("EventFilter.HcalRawToDigi.HcalRawToDigi_cfi")
#------------------------------------------------------------------------------------
# Set up our analyzer
#------------------------------------------------------------------------------------
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_cfi") # loads all modules
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Trigger_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HBHERecHits_CollisionData_cfi")
## set desired parameters, for example:
process.hcalTupleHFDigis.DoEnergyReco = False
process.hcalTupleHFDigis.FilterChannels = False
#process.hcalTupleHBHERecHits.source = cms.untracked.InputTag("hbheplan1")
#process.hcalTupleHBHERecHits.source = cms.untracked.InputTag("hbheprereco::PFG")
process.hcalTupleHBHERecHits.source = cms.untracked.InputTag("hbheprereco")
process.hcalTupleHBHERecHitsMethod0.source = cms.untracked.InputTag("hbheprereco")
process.hcalTupleHBHEDigis.recHits = cms.untracked.InputTag("hbheprereco")
#process.hcalTupleHBHEDigis.DoEnergyReco = cms.untracked.bool(False)
#process.hcalTupleHBHEDigis.DoEnergyReco = cms.untracked.bool(False)
process.hcalTupleHFDigis.ChannelFilterList = cms.untracked.VPSet(
    # Notice only channels listed here will be saved, if the FilterChannels flag is set to true
    cms.PSet(iEta = cms.int32(29), iPhi = cms.int32(39), depth = cms.int32(1)),
    )

from Configuration.StandardSequences.RawToDigi_Data_cff import *
process.CustomizedRawToDigi = cms.Sequence(
        gtDigis*
        #siPixelDigis*
        #siStripDigis*
        #ecalDigis*
        #ecalPreshowerDigis*
        hcalDigis
        #muonDTDigis*
        #muonCSCDigis*
        #muonRPCDigis*
        #castorDigis*
        #scalersRawToDigi*
        #tcdsDigis
)

#------------------------------------------------------------------------------------
# FED numbers 
#------------------------------------------------------------------------------------
#process.hcalDigis.FEDs = cms.untracked.vint32(	1100, 1102, 1104, # HBHEa 
#                                              	1106, 1108, 1110, # HBHEb
#                                              	1112, 1114, 1116, # HBHEc
#                                              	1118, 1120, 1122, # HF
#                                              	1119, 1121, 1123  # HF
#					        724, 725, 726, 727, 728, 729, 730, 731, # HO
# 					        1134 # HcalLaser
#                                              )

#------------------------------------------------------------------------------------
# QIE10  Unpacker
#------------------------------------------------------------------------------------
process.qie10Digis = process.hcalDigis.clone()
#process.qie10Digis.FEDs = cms.untracked.vint32(1118,1120,1122,1119,1121,1123)

#------------------------------------------------------------------------------------
# QIE11  Unpacker
#------------------------------------------------------------------------------------
process.qie11Digis = process.hcalDigis.clone()
#process.qie11Digis.InputLabel = cms.InputTag("source") 
#process.qie11Digis.FEDs = cms.untracked.vint32(1114)

#------------------------------------------------------------------------------------
# Specify Global Tag
#------------------------------------------------------------------------------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
#process.GlobalTag.globaltag = '101X_dataRun2_HLT_v7'
process.GlobalTag.globaltag = '101X_dataRun2_Prompt_v9'
print "GlobalTag = ", str(process.GlobalTag.globaltag).split("'")[1]
print " "

#------------------------------------------------------------------------------------
# Create Noise Filter
#------------------------------------------------------------------------------------
# Could be out of date, commented out in the main sequence, need to be fixed
#process.hcalnoise.fillCaloTowers = cms.bool(False)
#process.hcalnoise.fillTracks = cms.bool(False)
#process.ApplyBaselineHBHENoiseFilter = cms.EDFilter(
#    'BooleanFlagFilter',
#    inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),
#    reverseDecision = cms.bool(False)
#    )

#------------------------------------------------------------------------------------
# HcalTupleMaker sequence definition
#------------------------------------------------------------------------------------
process.tuple_step = cms.Sequence(
    ## Make HCAL tuples: Event info
    process.hcalTupleEvent*
    
    ## Make HCAL tuples: FED info
    #process.hcalTupleFEDs*
    
    ## Make HCAL tuples: digi info
    process.hcalTupleHBHEDigis*
    #process.hcalTupleHODigis*
#    process.hcalTupleHFDigis*
#    process.hcalTupleQIE10Digis* # for HF
#    process.hcalTupleQIE11Digis* # for HEP17
    
    ## Make HCAL tuples: reco info
#    process.hcalTupleHBHERecHits*
    #process.hcalTupleHFRecHits*
    #process.hcalTupleHORecHits*
    #process.hcalTupleHFRecHits*
    process.hcalTupleHBHERecHits*
    process.hcalTupleHBHERecHitsMethod0*
    ## Make HCAL tuples: trigger info
    #process.hcalTupleTrigger*
    #process.hcalTupleTriggerPrimitives*
    #process.hcalTupleTriggerObjects*

    ## Package everything into a tree
    process.hcalTupleTree
)

#-----------------------------------------------------------------------------------
# Define the recoPath
#-----------------------------------------------------------------------------------
#process.recoPath = cms.Path(
#    process.hbheprereco
#    *process.hbhereco
#)


process.dump = cms.EDAnalyzer("EventContentAnalyzer")

#-----------------------------------------------------------------------------------
# Path and EndPath definitions
#-----------------------------------------------------------------------------------
process.preparation = cms.Path(
    ## Unpack digis from RAW
    #process.RawToDigi*
    #process.CustomizedRawToDigi*
    #process.gtDigis*
    process.hcalDigis*
#    process.recoPath*
#    process.qie10Digis*
    #process.qie11Digis*
    
    ## reconstruction 
    #process.L1Reco*
    #process.reconstruction*
    #process.hcalLocalRecoSequence*
    
    ## Do energy reconstruction
    #process.horeco*
    #process.hfprereco*
    #process.hfreco*
    process.hbheprereco*
    #process.hbheplan1*
    #process.hbhereco*
    #process.hcalTupleHBHERecHits*
    #process.hcalTupleHBHERecHitsMethod0*
    
    ## For noise filter
    #process.hcalnoise*
    #process.HBHENoiseFilterResultProducer*
    #process.ApplyBaselineHBHENoiseFilter*
    
    ## Make the ntuples
    process.tuple_step
#    process.dump
)

#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('293765:264-293765:9999')
