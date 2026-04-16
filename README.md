# SDN-Based Flow Rule Timeout Manager (POX)

## 📌 Problem Statement
The goal is to implement an SDN solution using the POX controller to manage the lifecycle of flow entries. By utilizing Idle Timeouts, the system automatically purges inactive rules from the switch's flow table, preventing resource exhaustion and ensuring efficient TCAM utilization.

## 🛠️ Tools Used
- **Mininet**: Network Emulator.
- **POX Controller**: Python-based SDN Controller.
- **Open vSwitch**: Virtual Switch.
- **Ubuntu**: Linux VM Environment.

## 🌐 Network Topology
- **Single Switch Topology**: 1 Switch (`s1`) and 3 Hosts (`h1`, `h2`, `h3`).
- **Controller**: Remote POX controller.

## ⚙️ Execution Steps

### Step 1: Save the Controller Script
Place your script in the `pox/ext/` directory as `timeout_manager.py`. Ensure your `ofp_flow_mod` includes:
```python
msg.idle_timeout = 20


### Step 2: Start POX Controller
bash
cd ~/pox
./pox.py log.level --DEBUG misc.timeout_manager


### Step 3: Start Mininet
bash
sudo mn -c
sudo mn --topo single,4 --controller=remote

*Note: This terminal shows the creation of hosts `h1` through `h3` and switch `s1`.*


## 🧪 Test Cases

| Test Scenario          | Command                      | Expected Result |
| **Connectivity**       | `h1 ping -c 4 h2`            | 0% packet loss. |
| **Flow Installations** | `sh ovs-ofctl dump-flows s1` | Rule exists with `idle_timeout=20`.|
| **Rule Expiration**    | Wait 25 Seconds              | Flow table becomes empty.|

## 📊 Flow Rule Implementation
- **Event Handling**: Controller handles `PacketIn` events.
- **Match Logic**: Source/Destination MAC and IP matching.
- **Action**: `ofp_action_output` to the correct port.
- **Timeout**: `idle_timeout` set to 20 seconds to manage rule lifecycle.

## 📈 Performance & Validation
- **Latency**: Initial ARP/PacketIn request shows higher RTT; subsequent pings use the installed flow rule.
- **Dynamic Management**: Verified that rules are only present when traffic is active, proving successful timeout-based eviction.



## 🧠 Conclusion
This project demonstrates that SDN allows for granular, automated control over switch resources. Using POX to set flow timeouts ensures that the network remains performant by preventing the accumulation of stale rules.

👩‍💻 Author
Srinidhi P
PES University
