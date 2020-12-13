# 802dot11

This Repository was created as final project of the subject "Data Comunication" of the MSC in Telecommuinications of UNC.

In this  PoC I developed a software system for remote access  points (Aps) monitoring of IEEE 802.11 wirless local area networks (WLANs). It collects basic parameters in physical (PHY) layer as well as medium access control (MAC) layer. This system allows through a raspberry pi device setted up in monitor mode to save pcap  files with beacon frames (BFs) transmitted by APs, these BFs are sent using a socket connection to a remote server and inserted in a database. A web service was implemented to visualize service set identifier (SSID), Received Signal Strength Indication (RSSI), media access control address (MAC address), timestamp, and Channel number. Also the information visualized can be instantaneous and historical. Measures were done in a not controlled indoor environment.
