#ifndef RecoLocalTracker_SiPhase2Clusterizer_Phase2TrackerReclusterizerAlgorithm_h
#define RecoLocalTracker_SiPhase2Clusterizer_Phase2TrackerReclusterizerAlgorithm_h

#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"

// digis used later for bad strip access
#include "DataFormats/Phase2TrackerDigi/interface/Phase2TrackerDigi.h"
#include "DataFormats/Phase2TrackerCluster/interface/Phase2TrackerCluster1D.h"
#include "CondFormats/SiStripObjects/interface/SiStripBadStrip.h"

class Phase2TrackerReclusterizerAlgorithm {

public:

  // constructor is implicit, as there's no action to be taken
  inline void reclusterize(const edmNew::DetSet<Phase2TrackerCluster1D>&,             
                            Phase2TrackerCluster1DCollectionNew::FastFiller&,
                            const bool, const SiStripBadStrip*, const int) const;

};

void Phase2TrackerReclusterizerAlgorithm::reclusterize(
    const edmNew::DetSet<Phase2TrackerCluster1D>& inputClustersModuleIter,
    Phase2TrackerCluster1DCollectionNew::FastFiller& clusterFiller,
    const bool handleBadStrips_,
    const SiStripBadStrip* badStripPayload_,
    const int maxBadStrips
) const {
  
  if (inputClustersModuleIter.empty()) return;

  auto cl = inputClustersModuleIter.begin();

  //Phase2TrackerCluster1D firstCluster = *cl;
  int sizeCluster = cl->size();
  Phase2TrackerDigi firstClusterDigi = cl->firstDigi();
  bool thresholdCluster = cl->threshold();
  
  ++cl;

  // there will always be a payload even if it's empty
  // Range is typedef for std::pair<std::vector<unsigned int>::const_iterator,std::vector<unsigned int>::const_iterator>
  // second element in pair is one past the last element in first element (open end)
  SiStripBadStrip::Range badStripObjects = badStripPayload_->getRange(inputClustersModuleIter.detId());
  // can be typedef to ContainerIterator
  std::vector<unsigned int>::const_iterator badStripObject = badStripObjects.first;

  for (; cl != inputClustersModuleIter.end(); ++cl) {
    
    Phase2TrackerDigi nextClusterDigi = cl->firstDigi();

    // only merge on the same column
    if ((firstClusterDigi.column() == nextClusterDigi.column())){
      
      // one past the last channel of the cluster
      const int firstClusterEdge = firstClusterDigi.channel() + sizeCluster;
      const int nextClusterFirst = nextClusterDigi.channel();

      // directly neighboring
      if(firstClusterEdge == nextClusterFirst){
        sizeCluster += cl->size();
        thresholdCluster |= cl->threshold();
      }else if(handleBadStrips_ &&
        (firstClusterEdge + maxBadStrips >= nextClusterFirst)
      ){

        // merging clusters with bad strips between them
        bool mergeWithBadStrips = false;
        
        // iterate over bad strips to find if there's a bad strip block
        // between the two clusters
        for(; badStripObject != badStripObjects.second; ++badStripObject){
          
          const auto badStripObjectDecoded = badStripPayload_->decodePhase2(*badStripObject);
          // decoded to packed channel (same as digi)
          const auto badStripChannel = badStripObjectDecoded.firstStrip;
          const auto badStripBlockSize = badStripObjectDecoded.range;
          const auto badStripEdge = badStripChannel + badStripBlockSize;
          
          if(badStripEdge <= firstClusterEdge) continue;

          // strict matching, block of bad strips within the gap
          // no under/overflow
          if(badStripChannel == firstClusterEdge &&
            badStripEdge  == nextClusterFirst){
            mergeWithBadStrips = true;
            sizeCluster = sizeCluster + badStripBlockSize + cl->size();
            thresholdCluster |= cl->threshold();

            std::cout << "Merging cluster with edge " << firstClusterEdge << " to cluster with first strip " << nextClusterFirst << " separated by bad strip block with channel " << badStripChannel << " and size " << badStripBlockSize << std::endl;
          }           

          break;
          
        }
        
        if(!mergeWithBadStrips){
          clusterFiller.push_back(Phase2TrackerCluster1D(firstClusterDigi, sizeCluster, thresholdCluster));
          firstClusterDigi = nextClusterDigi;
          sizeCluster = cl->size();
          thresholdCluster = cl->threshold();               
        }

      }else{

        clusterFiller.push_back(Phase2TrackerCluster1D(firstClusterDigi, sizeCluster, thresholdCluster));
        firstClusterDigi = nextClusterDigi;
        sizeCluster = cl->size();
        thresholdCluster = cl->threshold();               

      }

    }else{
      
      clusterFiller.push_back(Phase2TrackerCluster1D(firstClusterDigi, sizeCluster, thresholdCluster));
      firstClusterDigi = nextClusterDigi;
      sizeCluster = cl->size();
      thresholdCluster = cl->threshold();               
      
    }


  }

  clusterFiller.push_back(Phase2TrackerCluster1D(firstClusterDigi, sizeCluster, thresholdCluster));

}

#endif