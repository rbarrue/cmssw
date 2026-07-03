#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/Phase2TrackerCluster/interface/Phase2TrackerCluster1D.h"

// #include "Phase2TrackerReclusterizerAlgorithm.h"

class Phase2TrackerReclusterizer : public edm::stream::EDProducer<> {
public:

    explicit Phase2TrackerReclusterizer(const edm::ParameterSet& conf);
    ~Phase2TrackerReclusterizer() override = default;

    void produce(edm::Event& event, const edm::EventSetup& eventSetup) override;

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
    
    // these have the natural detId ordering from DetSetVec
    // since Phase2TrackerCluster1DCollectionNew is just a typedef
    // to edmNew::DetSetVector<Phase2TrackerCluster1D>
    edm::EDGetTokenT<Phase2TrackerCluster1DCollectionNew> token_;

};

Phase2TrackerReclusterizer::Phase2TrackerReclusterizer(edm::ParameterSet const& conf)
    :
        token_(consumes<Phase2TrackerCluster1DCollectionNew>(conf.getParameter<edm::InputTag>("src"))) {
            produces<Phase2TrackerCluster1DCollectionNew>();
        }

void Phase2TrackerReclusterizer::produce(edm::Event& event, const edm::EventSetup& eventSetup) {

    edm::Handle<Phase2TrackerCluster1DCollectionNew> inputClustersFullDet;

    event.getByToken(token_, inputClustersFullDet);

    auto outputClustersFullDet = std::make_unique<Phase2TrackerCluster1DCollectionNew>();

    // Loops over each module
    for (const auto& inputClustersModuleIter : *inputClustersFullDet){
        
        // need to look a bit into this API
        Phase2TrackerCluster1DCollectionNew::FastFiller clusterFiller(*outputClustersFullDet, inputClustersModuleIter.detId());


        // TODO: create Reclusterizer algorithm class and
        
        // TODO: fix compilation errors
        
        // Phase2TrackerReclusterizerAlgorithm algo;
        // algo.reclusterize(inputClustersModuleIter, clusterFiller);

        // why this ?
        if (clusterFiller.empty()) clusterFiller.abort();

    }

    outputClustersFullDet->shrink_to_fit();
    event.put(std::move(outputClustersFullDet));

}

void Phase2TrackerReclusterizer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("siPhase2ClustersUnrefined"));
  descriptions.add("default_phase2TrackerReclusterizer", desc);
}

DEFINE_FWK_MODULE(Phase2TrackerReclusterizer);