import streamlit as st
import random

# ── DATA ────────────────────────────────────────────────────────────────────
PROF_PAPERS = {
    "D.K. Lobiyal": [
        "Cross-layer optimization using two-level dual decomposition in multi-flow ad-hoc networks",
        "Ant based Pareto Optimal Solution for QoS aware Energy Efficient Multicast in Wireless Networks",
        "Levenberg-Marquardt optimization method for coverage and connectivity in backbone based wireless networks",
        "T-MQM: Testbed-Based Multi-Metric Quality Measurement of Sensor Deployment for Precision Agriculture",
        "Cloud Computing in VANETs: Layered Architecture, Element, Taxonomy and Challenges",
        "Bezier Curve based Lupas (p,q) Analogue of Bernstein Functions in CAGD",
        "An Elitist Nondominated Sorting Genetic Algorithm for QoS Multicast Routing in Wireless Networks",
        "Novel DV-Hop Localization Algorithm in WSNs",
        "Evaluation of Message Dissemination Techniques in Vehicular Ad Hoc Networks",
        "Performance Evaluation of Mobile WiMAX IEEE 802.16e for Hard Handover",
        "Coverage Probability using EM Waves for UWSN in Shadowing Environment",
        "Multipath Routing in Mobile Ad Hoc Network with Probabilistic Splitting of Traffic",
        "Multiobjective Dynamic Vehicle Routing Problem and Time Seed Based Solution Using PSO",
        "Fuzzy Hindi WordNet and Word Sense Disambiguation Using Fuzzy Graph Connectivity Measures",
        "Probabilistic Intrusion Detection in Randomly Deployed Wireless Sensor Networks",
        "Analytical Evaluation of Directional-Location Aided Routing Protocol for VANETs",
        "Coupling Strength and Seizures",
        "Sensor node deployment and coverage prediction for underwater sensor networks",
        "Energy efficient reactive protocol for data aggregation in Wireless Sensor Network",
        "Concepts Extraction for Medical Documents using Ontology",
        "Unsupervised Hindi Word Sense Disambiguation based on network Agglomeration",
        "A New Method for Updating Word Senses in Hindi WordNet",
        "Connectivity Enhancement in Randomly Distributed WSN Using Cooperative Cluster Transmission",
        "Minimum Energy Multicast in Static Wireless Ad Hoc Networks using Swarm Intelligence",
        "Power Efficient MAC Protocol for Mobile Ad hoc Networks",
        "Novel Transmission Time based Mechanism to Detect Wormhole Attacks",
        "Intersection area based geocasting protocol for Vehicular Ad hoc Networks",
        "Performance Evaluation of VANET using Realistic Vehicular Mobility",
        "Improved Position-Based Routing in VANETs using P-DIR Method",
        "Enhanced Efficient Broadcasting Scheme for Video-on-Demand System in MANETs",
        "Apis Mellifera Pre-miRNA Prediction using Decision Tree based Classifier",
        "Computational Grammar for Hindi",
        "Rule Based Natural Language Parser: An Object Oriented Approach",
        "IP Address Filtering to Control Congestion",
        "Database Technology and its Future Prospects",
    ],
    "D.P. Vidyarthi": [
        "Energy-efficient communication-aware VM placement in cloud datacenter using hybrid ACO-GWO",
        "PMRNA: Parameter matching of realtime and non-realtime applications for resource provisioning in fog-integrated cloud",
        "A hybrid model using JAYA-GA metaheuristics for placement of fog nodes in fog-integrated cloud",
        "Optimizing Fog Device Deployment for Maximal Network Connectivity and Edge Coverage",
        "An ML-based task clustering and placement using hybrid Jaya-gray wolf optimization in fog-cloud ecosystem",
        "FNSS: A Heuristics for Fog Node Site Selection",
        "Fog node placement using multi-objective genetic algorithm",
        "Communication-aware, energy-efficient VM placement in cloud data center using ant colony optimization",
        "A modified fuzzy similarity measure for trapezoidal fuzzy number with their applications",
        "Blockchain based resource allocation in cloud and distributed edge computing: A survey",
        "An efficient fuzzy-based task offloading in edge-fog-cloud architecture",
        "BARA: A blockchain-aided auction-based resource allocation in edge computing enabled IIoT",
        "TRAPPY: truthfulness and reliability aware application placement policy in fog computing",
        "Admission control and resource provisioning in fog-integrated cloud using modified fuzzy inference system",
        "Fair Resource Allocation Policies in Reverse Auction based Cloud Market",
        "BLOSOM: Blockchain technology for Security of Medical records",
        "FONS: a fog orchestrator node selection model to improve application placement in fog computing",
        "Heterogeneity aware elastic scaling of streaming applications on cloud platforms",
        "Artificial lizard search optimization (ALSO): a novel nature-inspired meta-heuristic algorithm",
        "A novel energy-efficient scheduling model for multi-core systems",
        "QoE Aware IoT Application Placement in Fog Computing Using Modified-TOPSIS",
        "Modified Dragonfly Algorithm for Optimal Virtual Machine Placement in Cloud Computing",
        "A framework for IoT Service Selection",
        "A Pricing Model for Effective Radio Spectrum Utilization",
    ],
    "Manju Khari": [
        "An evolutionary SVM model for DDOS attack detection in software defined networks",
        "Securing data in Internet of Things (IoT) using cryptography and steganography techniques",
        "Energy enhancement using Multiobjective Ant colony optimization with Double Q learning for IoT cognitive radio networks",
        "Enhanced resource allocation in mobile edge computing using reinforcement learning based MOACO for IIOT",
        "Empirical study of software defect prediction: a systematic mapping",
        "A holistic overview of deep learning approach in medical imaging",
        "HIIDS: Hybrid intelligent intrusion detection system empowered with machine learning and metaheuristic algorithms",
        "ARM-AMO: An efficient association rule mining algorithm based on animal migration optimization",
        "Gesture recognition of RGB and RGB-D static images using convolutional neural networks",
        "Detection of DDOS attack using deep learning model in cloud storage application",
        "Real-time image enhancement for automatic automobile accident detection through CCTV using deep learning",
        "A Blockchain Framework to Secure Personal Health Record (PHR) in IBM Cloud-Based Data Lake",
        "Fingerprint image enhancement and reconstruction using orientation and phase reconstruction",
        "Biometric iris recognition using radial basis function neural network",
        "Neutrosophic soft set decision making for stock trending analysis",
        "Assessment of code smell for predicting class change proneness using machine learning",
        "R-CNN and wavelet feature extraction for hand gesture recognition with EMG signals",
        "Blockchain in agriculture to ensure trust, effectiveness, and traceability from farm fields to groceries",
        "Optimized test suites for automated testing using different optimization techniques",
        "EESSMT: an energy efficient hybrid scheme for securing mobile ad hoc networks using IoT",
        "Internet of things and big data analytics for smart generation",
        "Internet of Things based system for Smart Kitchen",
        "3D face reconstruction from single 2D image using distinctive features",
        "Optimal routing strategy using extreme learning machine with beetle antennae search algorithm",
    ],
    "Piyush Pratap Singh": [
        "An Insight into Code Smell Detection Tool",
        "Impact Calculation of The Players Using the Cricket Commentary Corpus",
        "Maithili Text-to-Speech System",
        "Implementation of 6-W based precisiation structure for text summarization using VB .net",
        "Advancing Legal Document Summarization: A Recursive Summarization Algorithm Approach",
        "Advancements in legal text summarization: integrating InLegalBERT for effective extractive summarization",
        "Handwritten Telugu two-digit recognition and novel computational analysis of ancient fractional notations",
        "LegSegSC: A Silver-Standard Rhetorical Role Labeled Dataset of Indian Supreme Court Judgments",
    ],
    "R.K. Agrawal": [
        "Hybrid of Handcrafted and Learnable features using Multimodal Fusion Network for Brain tumor segmentation",
        "Metabolic and Structural Insights of Cerebellar Dysfunction in Spinocerebellar Ataxia Type 12",
        "MSST-EEGNet: Multi-scale spatio-temporal feature extraction using inception and temporal pyramid pooling",
        "Weighted fuzzy clustering with adaptive spatial information and KL divergence for skin lesion segmentation",
        "Noise and cluster size insensitive robust weighted fuzzy clustering for medical image segmentation",
        "Integration of graph network with kernel SVM for identification of biomarkers in SCA12",
        "Performance Evaluation of Thermography-Based Computer-Aided Diagnostic Systems for Detecting Breast Cancer",
        "IterMiUnet: A lightweight architecture for automatic blood vessel segmentation",
        "Fast and robust spatial fuzzy bounded k-plane clustering for human brain MRI segmentation",
        "Enhanced Depression Detection from Speech using Quantum Whale Optimization for Feature Selection",
        "Multi-objective particle swarm optimization with guided exploration for multimodal problems",
        "Fuzzy k-plane clustering with local spatial information for human brain MRI segmentation",
        "Bias-corrected intuitionistic fuzzy c-means with spatial neighbourhood for brain MRI segmentation",
        "Triploid genetic algorithm for convolutional neural network diagnosis of mild cognitive impairment",
        "Quantum inspired Particle Swarm Optimization with guided exploration for function optimization",
        "Power Spectral Techniques with Feature Selection for Mental Task Classification in Noninvasive BCI",
        "3-D discrete wavelet transform and 3-D local binary pattern for mild cognitive impairment classification",
        "Quantum based Whale Optimization Algorithm for Wrapper Feature Selection",
        "Kernel intuitionistic fuzzy entropy clustering for MRI image segmentation",
        "A hierarchical meta-model for multi-class mental task based brain-computer interfaces",
    ],
    "Ratneshwer": [
        "A robust weighted late fusion approach for IoT",
        "Uncertainty Modelling in Performability Prediction for Safety-Critical Systems",
        "A reward-based performability modelling of a fault-tolerant safety-critical system",
        "An Early Predictive and Recovery Mechanism for Scheduled Outages in Service-Based Systems",
        "Non-disruptive change management modeling of SOA based systems",
        "Scheduled Outage Tolerance for SOA-Based Systems Through Rule Based Approach",
        "A Literature Review on Fault Tolerance in SOA-based Systems",
        "Performability modeling of safety-critical systems through AADL",
        "Fault Prediction in SOA-Based Systems Using Deep Learning Techniques",
        "Fault diagnosis in service-oriented computing through partially observed stochastic Petri nets",
        "Systematic review of congestion handling techniques for 802.11 wireless networks",
        "An approach for fault prediction in SOA-based systems using machine learning techniques",
        "Fault Modelling of an Object-Oriented System using CPN",
        "Fault analysis of service-oriented systems: a systematic literature review",
        "Colored Petri Nets Based Fault Diagnosis in Service Oriented Architecture",
        "A Router based Hybrid Approach for Congestion Control in High speed Wired Networks",
        "Dependency Based Fault Diagnosis Approach for SOA Based Systems using Colored Petri Nets",
        "Extended Fault Taxonomy of SOA based Systems",
        "Ranking of Router-Based Congestion Control Approaches for High Speed Networks using AHP",
        "Congestion control for high-speed wired network: A systematic literature review",
        "A Review of End-to-end Congestion Control Algorithms for High-speed Wired Network",
        "A Knowledge Identification Framework for Component Based Dependency Analysis Process",
    ],
    "Satish Chand": [
        "Efficient Staircase Scheme with Seamless Channel Transition Mechanism",
        "Segmented Patching Broadcasting Protocol for Video Data",
        "Storage Space Estimation for Videos using Fading Channels",
        "SC- and SS- wavelet Transforms",
        "Video Data Delivery using Slotted Patching",
        "Efficient Generalized Conservative Staircase scheme for popular Videos",
        "Buffer Storage for Continuous Delivery of Video Data",
        "Phase Estimation in Data Channelization for Videos",
        "Patching-based Broadcasting Scheme for Video Services",
        "Efficient Utilization of Buffer Storage in Conservative Staircase Broadcasting Scheme",
        "Geometrico-Harmonic Data Broadcasting and receiving Scheme",
        "Geometrico-harmonic Broadcasting Scheme with Continuous Redundancy",
        "Modeling of Buffer Storage in Video Transmission",
        "Generalized Conservative Staircase Data Broadcasting Protocol for Video-on-Demand",
        "Seamless Channel Transition for Cautious Harmonic Scheme in Video Data Broadcasting",
        "Request based Data Delivery in Video-on Demand Services",
        "Modified Polyharmonic Data Broadcasting Scheme for Popular Videos",
        "Seamless Channel Transition Using Bespoke Broadcasting Scheme for Video-On-Demand Service",
        "Bespoke data broadcasting scheme for popular videos",
        "Buffer Evaluation in Variable Bandwidth Channelization for Videos",
        "Modified Bespoke data broadcasting scheme for popular videos",
        "Modified staircase data broadcasting scheme for popular videos",
    ],
    "Sonajharia Minz": [
        "CCRA: channel criticality based resource allocation in cognitive radio networks",
        "Multi-view Ensemble Learning: An optimal Feature set Partitioning for High Dimensional Data Classification",
        "Binarizing Change for Fast Trend Similarity Based Clustering of Time Series Data",
        "Change Detection Using Unsupervised Learning Algorithms for Delhi, India",
        "Heirarchical Privacy Preserving Distributed Frequent Itemset Mining (HPPDFIM)",
    ],
    "Vir Bahadur Singh": [
        "Enhanced payload and trade-off for image steganography via a novel pixel digits alteration",
        "Entropy based Software Reliability Growth Modelling for Open Source Evolution",
        "Multi-Attribute Dependent Bug Severity and Fix Time Prediction Modeling",
        "Quantitative Quality Evaluation of Software Products by Considering Summary and Comments Entropy of a Bug",
        "Entropy Based Software Reliability Analysis of Multi-Version Open Source Software",
        "Modeling and analysis of leftover issues and release time planning in multi-release open source software",
        "Severity Assessment of a Reported Bug by considering its Uncertainty and Irregular State",
        "Cost-reliability-optimal release time of software with patching considered",
        "Reduction of Redundant Rules in Association Rule Mining Based Bug Assignment",
        "An Estimation Technique in Agile Archetype using Story Points and Function Point Analysis",
        "Requirement Paradigms to Implement Software Projects in Agile Development using AHP",
        "Bug Severity Assessment In Cross Project Context and Identifying Training Candidates",
        "Clustering based Association Rule Mining for Bug Assignee Prediction",
        "Bug prediction modeling using the complexity of code changes",
        "Predicting the complexity of code changes using entropy based measures",
        "An Empirical evaluation of cross project priority prediction",
        "Generalized Reliability Model for Cloud Computing",
        "Quality Issues in Infrastructure as a Service",
    ],
    "Karan Singh": [
        "Joint beacon frequency and beacon transmission power adaptation for internet of vehicles",
        "Green communication in sensor-enabled IoT: integrated physics-inspired meta-heuristic optimization",
        "Cluster Based Localization Scheme with Backup Node in Underwater Wireless Sensor Network",
        "Energy Efficient Optimized Rate based Congestion Control Routing in Wireless Sensor Network",
        "Optimizing Compressive Sensing Matrix using Chicken Swarm Optimization Algorithm",
        "Lightweight Security Scheme for Internet of Things",
        "Congestion Control in Wireless Sensor Networks by Hybrid Multi-Objective Optimization Algorithm",
        "Modeling and Analysis of Worm Propagation in Wireless Sensor Networks",
        "Cryptanalysis and Improvement in User Authentication and Key Agreement Scheme for WSN",
        "Kullback-Leibler Divergence and Background Subtraction for Moving Object Detection in Thermal Video",
        "Efficient Multicast Congestion Control",
        "A Novel and Comprehensive Trust Estimation Clustering Based Approach for Large Scale WSNs",
        "An Intelligent Scheme for Continuous Authentication of Smartphone Using Deep Auto Encoder",
        "Effective algorithm for optimizing compressive sensing in IoT and periodic monitoring applications",
        "Quality, Reliability, Security and Robustness in Heterogeneous Networks",
    ],
    "Sushil Kumar": [
        "Towards precision agriculture: IoT-enabled intelligent irrigation systems using deep learning neural network",
        "Ant colony optimization based QoS aware energy balancing secure routing for wireless sensor networks",
        "Mycosporine and mycosporine-like amino acids: A paramount tool against ultra violet irradiation",
        "Cybersecurity risk analysis of electric vehicles charging stations",
        "MCFT-CNN: Malware classification with fine-tune convolution neural networks using traditional and transfer learning in IoT",
        "An emerging threat fileless malware: a survey and research challenges",
        "Virtualization in wireless sensor networks: Fault tolerant embedding for internet of things",
        "Breaking the data barrier: a review of deep learning techniques for democratizing AI with small datasets",
        "Cloud computing in VANETs: architecture, taxonomy, and challenges",
        "Geometry-based localization for GPS outage in vehicular cyber physical systems",
        "T-MQM: Testbed-based multi-metric quality measurement of sensor deployment for precision agriculture",
        "Delimitated anti jammer scheme for Internet of vehicle: Machine learning based security approach",
        "Medium access control (MAC) for wireless body area network (WBAN): taxonomy and challenges",
        "Multiobjective dynamic vehicle routing problem and time seed based solution using particle swarm optimization",
        "Trust evaluation for light weight security in sensor enabled IoT: game theory oriented approach",
        "Cross-layer energy optimization for IoT environments: Technical advances and opportunities",
        "Toward energy-oriented optimization for green communication in sensor enabled IoT environments",
        "Energy balanced position-based routing for lifetime maximization of wireless sensor networks",
        "Sensing coverage prediction for wireless sensor networks in shadowed and multipath environment",
        "BEST: blockchain-enabled secure and trusted public emergency services for smart cities",
    ],
    "Buddha Singh": [
        "Traffic-Aware Density-Based Sleep Scheduling and Energy Modeling for 2D Gaussian Distributed WSN",
        "An Energy-Efficient Adaptive Clustering Algorithm with Load Balancing for Wireless Sensor Network",
        "A Novel Energy-Aware Cluster Head Selection based on PSO for Wireless Sensor Networks",
        "A MAC-Layer Packet Retransmission Technique for Minimizing Energy Consumption in WSN",
        "Energy Preserving Sleep Scheduling for Cluster-based Wireless Sensor Networks",
    ],
}

ALL_PROFS = list(PROF_PAPERS.keys())

# ── HELPERS ──────────────────────────────────────────────────────────────────
def weighted_prof_pick():
    counts  = {p: len(papers) for p, papers in PROF_PAPERS.items()}
    max_c   = max(counts.values())
    weights = {p: (max_c - counts[p] + 1) ** 0.7 for p in ALL_PROFS}
    total   = sum(weights.values())
    r, cumulative = random.random() * total, 0
    for p, w in weights.items():
        cumulative += w
        if r <= cumulative:
            return p
    return ALL_PROFS[-1]

def generate_question():
    correct = weighted_prof_pick()
    paper   = random.choice(PROF_PAPERS[correct])
    others  = [p for p in ALL_PROFS if p != correct]
    random.shuffle(others)
    options = [correct] + others[:2]
    random.shuffle(options)
    return paper, correct, options

def difficulty_label(prof):
    n = len(PROF_PAPERS[prof])
    if n <= 5:   return "🔥 Hard",   "#ff6b6b"
    if n <= 12:  return "⚡ Medium", "#f9c74f"
    return "✅ Easy", "#4cc98c"

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Know Your Prof 🎓",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── FIREWORKS CANVAS HTML ────────────────────────────────────────────────────
FIREWORKS_HTML = """
<canvas id="fw-canvas" style="
  position:fixed;top:0;left:0;
  width:100vw;height:100vh;
  pointer-events:none;z-index:99999;
"></canvas>
<script>
(function(){
  const C   = document.getElementById('fw-canvas');
  const ctx = C.getContext('2d');
  C.width   = window.innerWidth;
  C.height  = window.innerHeight;
  const W   = C.width, H = C.height;

  const COLS = ['#f9c74f','#f8961e','#f3722c','#4cc98c',
                '#4895ef','#ff6b9d','#c77dff','#ffffff',
                '#ff4d6d','#06d6a0','#ffd166','#ef476f'];

  function Particle(ox, oy) {
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 16 + 3;
    this.x  = ox; this.y = oy;
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed - Math.random() * 6;
    this.g  = 0.48;
    this.col   = COLS[Math.floor(Math.random() * COLS.length)];
    this.alpha = 1;
    this.decay = Math.random() * 0.013 + 0.007;
    this.size  = Math.random() * 10 + 4;
    this.type  = Math.floor(Math.random() * 3);
    this.rot   = Math.random() * Math.PI * 2;
    this.rs    = (Math.random() - 0.5) * 0.28;
  }
  Particle.prototype.tick = function(){
    this.vy   += this.g;
    this.x    += this.vx;
    this.y    += this.vy;
    this.vx   *= 0.97;
    this.alpha -= this.decay;
    this.rot  += this.rs;
  };
  Particle.prototype.draw = function(){
    ctx.save();
    ctx.globalAlpha = Math.max(0, this.alpha);
    ctx.fillStyle   = this.col;
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rot);
    if (this.type === 0) {
      ctx.fillRect(-this.size/2, -this.size/4, this.size, this.size/2);
    } else if (this.type === 1) {
      ctx.beginPath();
      ctx.arc(0, 0, this.size/2.2, 0, Math.PI*2);
      ctx.fill();
    } else {
      const n=5, s=this.size/2, r=s*0.42;
      ctx.beginPath();
      for(let i=0;i<n*2;i++){
        const a=(i*Math.PI)/n - Math.PI/2;
        const rad = i%2===0 ? s : r;
        i===0 ? ctx.moveTo(Math.cos(a)*rad, Math.sin(a)*rad)
              : ctx.lineTo(Math.cos(a)*rad, Math.sin(a)*rad);
      }
      ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  };

  const ORIGINS = [
    [W*.22, H*.42], [W*.78, H*.42],
    [W*.50, H*.52], [W*.12, H*.30],
    [W*.88, H*.30], [W*.50, H*.22],
  ];

  let parts = [];
  // staggered bursts
  ORIGINS.forEach(([x,y], i) => {
    setTimeout(() => {
      for(let k=0;k<80;k++) parts.push(new Particle(x, y));
    }, i * 160);
  });

  function loop(){
    ctx.clearRect(0, 0, W, H);
    parts = parts.filter(p => p.alpha > 0.01);
    parts.forEach(p => { p.tick(); p.draw(); });
    if(parts.length > 0) requestAnimationFrame(loop);
    else { ctx.clearRect(0,0,W,H); C.remove(); }
  }
  requestAnimationFrame(loop);
})();
</script>
"""

# ── STYLES ───────────────────────────────────────────────────────────────────
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Syne:wght@800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

/* bg */
.stApp {
  background: radial-gradient(ellipse at 20% 0%, #1e1250 0%, #0d0b1e 45%),
              radial-gradient(ellipse at 80% 100%, #0d1b2a 0%, #0d0b1e 60%);
  min-height: 100vh;
}

/* strip streamlit chrome */
header[data-testid="stHeader"] { display:none!important; }
footer                          { display:none!important; }
#MainMenu                       { display:none!important; }
.block-container {
  padding: 0.8rem 0.7rem 3rem !important;
  max-width: 500px !important;
  margin: 0 auto !important;
}

/* header */
.hdr { text-align:center; padding:0.9rem 0.4rem 0.5rem; }
.hdr h1 {
  font-family:'Syne',sans-serif;
  font-size: clamp(1.55rem,6.5vw,2.3rem);
  font-weight:800;
  background:linear-gradient(90deg,#f9c74f,#f8961e,#f3722c);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  margin:0; line-height:1.15;
}
.hdr p { color:#7a8baa; font-size:0.82rem; margin:0.25rem 0 0; font-weight:600; }

/* stats */
.stat-row {
  display:flex; justify-content:center;
  gap:0.45rem; margin:0.6rem 0 0.4rem; flex-wrap:wrap;
}
.stat-pill {
  background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.11);
  border-radius:99px;
  padding:0.22rem 0.8rem;
  color:#7a8baa; font-size:0.75rem; font-weight:700;
}
.stat-pill b { color:#e9ecf5; }

/* streak */
.streak-row { display:flex; justify-content:center; gap:5px; margin:0.35rem 0 0.75rem; }
.sd {
  width:11px; height:11px; border-radius:50%;
  background:rgba(255,255,255,0.1);
  border:1px solid rgba(255,255,255,0.16); flex-shrink:0;
}
.sd.ok  { background:#4cc98c; box-shadow:0 0 8px #4cc98c99; }
.sd.bad { background:#ff6b6b; box-shadow:0 0 8px #ff6b6b88; }

/* paper card */
.paper-card {
  background:rgba(255,255,255,0.055);
  border:1px solid rgba(255,255,255,0.12);
  border-radius:20px;
  padding:1.2rem 1.1rem 1rem;
  margin:0 0 0.9rem;
  backdrop-filter:blur(16px);
  box-shadow:0 10px 40px rgba(0,0,0,0.5);
}
.paper-meta {
  display:flex; align-items:center;
  gap:0.45rem; margin-bottom:0.5rem;
}
.paper-tag {
  font-size:0.62rem; letter-spacing:.14em;
  text-transform:uppercase; color:#f9c74f; font-weight:800;
}
.diff-chip {
  font-size:0.63rem; font-weight:800;
  padding:.14rem .55rem; border-radius:99px;
  border:1.5px solid currentColor; opacity:.9; margin-left:auto;
}
.paper-title {
  color:#e5eaf5;
  font-size:clamp(0.86rem,3.6vw,1.03rem);
  font-weight:700; line-height:1.55;
}

/* q label */
.q-label {
  color:#7a8baa; font-size:0.8rem; font-weight:700;
  text-align:center; margin:0 0 0.45rem;
}

/* option buttons – stacked, full-width */
div[data-testid="stVerticalBlock"] .stButton > button {
  width:100% !important;
  border-radius:15px !important;
  font-family:'Nunito',sans-serif !important;
  font-weight:700 !important;
  font-size:clamp(0.82rem,3.4vw,0.97rem) !important;
  padding:0.8rem 1rem !important;
  border:1.5px solid rgba(255,255,255,0.16) !important;
  background:rgba(255,255,255,0.065) !important;
  color:#d8e0f0 !important;
  line-height:1.35 !important;
  white-space:normal !important;
  word-break:break-word !important;
  min-height:3.3rem !important;
  margin-bottom:0.4rem !important;
  transition:all .16s ease !important;
  text-align:center !important;
}
div[data-testid="stVerticalBlock"] .stButton > button:hover {
  background:rgba(249,199,79,.17) !important;
  border-color:#f9c74f !important;
  color:#f9c74f !important;
  transform:translateY(-2px) !important;
  box-shadow:0 4px 18px rgba(249,199,79,.22) !important;
}
div[data-testid="stVerticalBlock"] .stButton > button:active {
  transform:scale(.97) !important;
}

/* feedback */
.fb-ok {
  background:linear-gradient(135deg,rgba(76,201,140,.22),rgba(76,201,140,.07));
  border:1.5px solid #4cc98c; border-radius:18px;
  padding:1.1rem 1rem; text-align:center;
  color:#4cc98c;
  font-size:clamp(1rem,4.2vw,1.25rem); font-weight:800;
  margin:0.3rem 0 0.8rem;
  animation:popIn .3s ease;
}
.fb-no {
  background:linear-gradient(135deg,rgba(255,107,107,.18),rgba(255,107,107,.05));
  border:1.5px solid #ff6b6b; border-radius:18px;
  padding:1rem; text-align:center;
  color:#ffb3b3;
  font-size:clamp(0.86rem,3.5vw,1.03rem); font-weight:700;
  margin:0.3rem 0 0.8rem;
  animation:shakeX .4s ease;
}
.fb-no .ans { color:#ff8080; font-weight:800; }

@keyframes popIn {
  0%   {transform:scale(.85);opacity:0}
  65%  {transform:scale(1.07)}
  100% {transform:scale(1);opacity:1}
}
@keyframes shakeX {
  0%,100%{transform:translateX(0)}
  20%{transform:translateX(-9px)}
  40%{transform:translateX(9px)}
  60%{transform:translateX(-5px)}
  80%{transform:translateX(5px)}
}

/* next button */
.stButton > button[kind="primary"] {
  background:linear-gradient(135deg,#f9c74f,#f8961e) !important;
  color:#1a1a2e !important; border:none !important;
  font-family:'Nunito',sans-serif !important;
  font-weight:800 !important; font-size:1rem !important;
  padding:0.8rem 1.5rem !important;
  border-radius:15px !important;
  box-shadow:0 4px 22px rgba(249,199,79,.38) !important;
  width:100% !important;
}

/* footer */
.footer {
  text-align:center; color:#2e3a50;
  font-size:0.7rem; margin-top:1.5rem; padding-bottom:1rem;
}
</style>
"""

# ── SESSION STATE ─────────────────────────────────────────────────────────────
def new_question():
    paper, correct, options = generate_question()
    st.session_state.paper    = paper
    st.session_state.correct  = correct
    st.session_state.options  = options
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.fireworks = False

if "paper" not in st.session_state:
    new_question()
    st.session_state.total   = 0
    st.session_state.score   = 0
    st.session_state.history = []

# ── RENDER ────────────────────────────────────────────────────────────────────
st.markdown(STYLES, unsafe_allow_html=True)

# 🎆 Fireworks — inject at very top so canvas is always on top
if st.session_state.get("fireworks"):
    st.markdown(FIREWORKS_HTML, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hdr">
  <h1>🎓 Know Your Prof?</h1>
  <p>Match the paper → the professor who wrote it</p>
</div>
""", unsafe_allow_html=True)

# Stats row
total = st.session_state.total
score = st.session_state.score
acc   = f"{int(score/total*100)}%" if total > 0 else "—"
st.markdown(f"""
<div class="stat-row">
  <div class="stat-pill">Asked <b>{total}</b></div>
  <div class="stat-pill">Correct <b>{score}</b></div>
  <div class="stat-pill">Accuracy <b>{acc}</b></div>
</div>
""", unsafe_allow_html=True)

# Streak dots (last 10)
hist = st.session_state.history[-10:]
dots = "".join(f'<div class="sd {"ok" if h else "bad"}"></div>' for h in hist)
dots += "".join('<div class="sd"></div>' for _ in range(10 - len(hist)))
st.markdown(f'<div class="streak-row">{dots}</div>', unsafe_allow_html=True)

# Paper card
d_label, d_color = difficulty_label(st.session_state.correct)
st.markdown(f"""
<div class="paper-card">
  <div class="paper-meta">
    <span class="paper-tag">📄 Research Paper</span>
    <span class="diff-chip" style="color:{d_color}">{d_label}</span>
  </div>
  <div class="paper-title">"{st.session_state.paper}"</div>
</div>
""", unsafe_allow_html=True)

# ── Answer buttons (stacked vertically — thumb-friendly) ─────────────────────
if not st.session_state.answered:
    st.markdown('<p class="q-label">👇 Which professor wrote this paper?</p>', unsafe_allow_html=True)
    for i, opt in enumerate(st.session_state.options):
        if st.button(opt, key=f"opt_{i}", use_container_width=True):
            st.session_state.answered = True
            st.session_state.selected = opt
            st.session_state.total   += 1
            if opt == st.session_state.correct:
                st.session_state.score   += 1
                st.session_state.history.append(True)
                st.session_state.fireworks = True
            else:
                st.session_state.history.append(False)
                st.session_state.fireworks = False
            st.rerun()

# ── Feedback ──────────────────────────────────────────────────────────────────
else:
    WIN  = ["🎉","❤️","🔥","⭐","🏆","✨","🎯","👏","💪","🥳","🎊","💥","🌟","🎆"]
    LOSE = ["😬","🤔","💭","📚","🧐","😅","🫠"]

    if st.session_state.selected == st.session_state.correct:
        e = random.choice(WIN)
        st.markdown(f"""
        <div class="fb-ok">
          {e} Nailed it! &nbsp;
          <span style="font-size:.88em;opacity:.8">Paper by</span> &nbsp;
          <span style="color:#fff">{st.session_state.correct}</span>
          &nbsp; {e}
        </div>
        """, unsafe_allow_html=True)
    else:
        e = random.choice(LOSE)
        st.markdown(f"""
        <div class="fb-no">
          {e} You picked <span class="ans">{st.session_state.selected}</span><br>
          This paper belongs to
          <b style="color:#fff">{st.session_state.correct}</b> &nbsp;📚
        </div>
        """, unsafe_allow_html=True)

    if st.button("➡️  Next Paper", type="primary", use_container_width=True):
        new_question()
        st.rerun()

st.markdown('<div class="footer">JNU CS Dept · Infinite Quiz · No scores, just knowledge 🎓</div>',
            unsafe_allow_html=True)
