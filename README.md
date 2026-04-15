🚀 SDN-Based Flow Rule Timeout Manager (POX)
📌 Problem Statement

The goal of this project is to implement a Software-Defined Networking (SDN) solution using the POX controller to manage the lifecycle of flow entries. By utilizing Idle Timeouts, the system automatically removes inactive rules from the switch's flow table. This prevents resource exhaustion, ensures efficient TCAM utilization, and improves overall network performance.

🛠️ Tools and Technologies Used
Tool	Description
Mininet	Network emulator for creating virtual networks
POX Controller	Python-based SDN controller
Open vSwitch (OVS)	Virtual switch supporting OpenFlow
Ubuntu	Linux Virtual Machine environment
Python	Programming language for controller development
🌐 Network Topology

Single Switch Topology

1 Switch: s1
4 Hosts: h1, h2, h3, h4
Controller: Remote POX Controller
        h1
         |
        ---
       | s1 |
        ---
      /  |  \
    h2  h3  h4

Controller: POX (Remote)
⚙️ Execution Steps
📍 Step 1: Save the Controller Script

Place the controller script inside the POX extension directory.

cd ~/pox/ext
nano timeout_manager.py

Ensure the following line is included in the ofp_flow_mod message:

msg.idle_timeout = 20
📍 Step 2: Start the POX Controller
cd ~/pox
./pox.py log.level --DEBUG misc.timeout_manager

Expected Output:

POX 0.7.0 (eel) is up.

This confirms that the controller is running and ready to accept switch connections.

📍 Step 3: Start Mininet
sudo mn -c
sudo mn --topo single,4 --controller=remote

Expected Output:

Hosts h1 to h4 and switch s1 are created.
The switch connects to the POX controller.
🧪 Test Cases
Test Scenario	Command	Expected Result
Connectivity Test	h1 ping -c 4 h2	0% packet loss
Flow Installation	sh ovs-ofctl dump-flows s1	Rule appears with idle_timeout=20
Flow Expiration	Wait 25 seconds	Flow table becomes empty
📊 Flow Rule Implementation
🔹 Event Handling
The POX controller handles PacketIn events triggered by switches.
🔹 Match Logic
Matches packets based on:
Source MAC Address
Destination MAC Address
Source and Destination IP
🔹 Actions

Forwards packets to the appropriate port using:

of.ofp_action_output(port=out_port)
🔹 Timeout Configuration

Implements automatic rule removal:

msg.idle_timeout = 20

This ensures that inactive flow entries are removed after 20 seconds.

📈 Performance and Validation
⏱️ Latency
The first packet experiences higher delay due to ARP resolution and PacketIn processing.
Subsequent packets experience reduced latency as flow rules are installed.
🔄 Dynamic Flow Management
Flow entries remain active only while traffic is present.
Inactive rules are automatically removed after the idle timeout.

This validates efficient and dynamic resource management in the SDN environment.

📸 Proof of Execution

Include the following screenshots in your repository:

Screenshot	Description
Controller Startup	POX controller loading the timeout_manager module
Mininet Nodes	Output of nodes and net commands
Active Flow Rule	ovs-ofctl dump-flows s1 showing idle_timeout=20
Expired Flow Rule	Empty flow table after 25 seconds
📂 Project Structure
SDN-Flow-Timeout-Manager/
│── pox/
│   └── ext/
│       └── timeout_manager.py
│
│── screenshots/
│   ├── controller_startup.png
│   ├── mininet_topology.png
│   ├── active_flow.png
│   └── expired_flow.png
│
└── README.md
🧠 Conclusion

This project demonstrates how Software-Defined Networking (SDN) enables granular and automated control over network resources. By configuring idle timeouts using the POX controller, stale flow entries are efficiently removed, ensuring optimal switch performance and effective TCAM utilization.

👩‍💻 Author

Srinidhi P
🎓 PES University
