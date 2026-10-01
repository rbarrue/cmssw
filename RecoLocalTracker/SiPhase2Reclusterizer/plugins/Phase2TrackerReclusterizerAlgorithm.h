#ifndef RecoLocalTracker_SiPhase2Clusterizer_Phase2TrackerReclusterizerAlgorithm_h
#define RecoLocalTracker_SiPhase2Clusterizer_Phase2TrackerReclusterizerAlgorithm_h

#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"

// digis used later for bad strip access
#include "DataFormats/Phase2TrackerDigi/interface/Phase2TrackerDigi.h"
#include "DataFormats/Phase2TrackerCluster/interface/Phase2TrackerCluster1D.h"

class Phase2TrackerReclusterizerAlgorithm {

public:

  // constructor is implicit, as there's no action to be taken
  inline void reclusterize(const edmNew::DetSet<Phase2TrackerCluster1D>&,             
                            Phase2TrackerCluster1DCollectionNew::FastFiller&) const;

};

void Phase2TrackerReclusterizerAlgorithm::reclusterize(
    const edmNew::DetSet<Phase2TrackerCluster1D>& inputClustersModuleIter,
    Phase2TrackerCluster1DCollectionNew::FastFiller& clusterFiller
) const {
  
  auto cl = inputClustersModuleIter.begin();

  Phase2TrackerCluster1D firstCluster = *cl;
  unsigned int sizeCluster = firstCluster.size();
  ++cl;

  for (; cl != inputClustersModuleIter.end(); ++cl) {  
    
    if ((firstCluster.column()==cl->column()) && (firstCluster.firstStrip()+sizeCluster == cl->firstStrip())){ 
      sizeCluster += cl->size();
    }else{
      
      clusterFiller.push_back(Phase2TrackerCluster1D(firstCluster.firstDigi(), sizeCluster));
      firstCluster = *cl;
      sizeCluster = cl->size();
      
    }


  }


}

#endif