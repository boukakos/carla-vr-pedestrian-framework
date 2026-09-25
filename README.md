**CARLA VR Pedestrian Framework**

Interactive VR pedestrian simulation built on top of CARLA Simulator, for pedestrian behavior and traffic safety studies. A VR-tracked player walks through a CARLA town while autonomous vehicles (via CARLA's Traffic Manager) detect and yield to them.

**What's in this repository**
**BP_MyPlayer_walker.uasset** — The Unreal Engine Blueprint for the VR player character. Contains:
- Room-scale VR locomotion (HMD-tracked movement, replacing keyboard/mouse when a headset is active)
- Desktop fallback controls (keyboard/mouse) for testing without a headset
- Camera height calibration for correct real-world scale in VR
- Collision setup for interaction with CARLA traffic
  
**human_in_the_loop.py** — Python script that connects to a running CARLA server and:
- Spawns autonomous vehicles under Traffic Manager control, configured to detect and yield to the player
- Spawns an invisible "proxy" CARLA pedestrian actor that tracks the VR player's real-time position, so the Traffic Manager (which only perceives official **walker.*** actors) can see and react to the player

**Requirements**
- CARLA: 0.9.15
- Unreal Engine: 4.26 (the version CARLA 0.9.15 is built against)
- Python: 3.7+ with the **carla** Python API package installed
- VR headset: Developed and tested with an HTC Vive (wired and wireless via the official HTC Vive Wireless Adapter), using SteamVR as the OpenVR runtime
- OS: Windows 10 (64-bit)
  
**Reference hardware**
Developed and tested on:
- CPU: Intel Core i7-9700K @ 3.60GHz (8 cores)
- GPU: NVIDIA GeForce RTX 4080 SUPER (16 GB dedicated VRAM)
- RAM: 32 GB

VR rendering is significantly more demanding than desktop preview — a dedicated GPU with adequate VRAM (comparable to or better than the above) is recommended for smooth performance with a full traffic load (40 vehicles).

**Setup notes**
- This project builds on an existing CARLA content setup (maps, base walker blueprints, project-specific triggers) that lives on the original development machine and is not included in this repository. **BP_MyPlayer_walker** is a child Blueprint of the project's base walker class — it needs to be placed inside a compatible CARLA/Unreal project to open correctly.
- The Blueprint expects a **CameraRoot → VRCamera** component hierarchy under the character's Capsule Component, with the camera height offset calibrated to the Capsule's half-height (see in-editor comments/defaults).
- **human_in_the_loop.py** connects to **localhost:2000** by default and expects a CARLA server (Editor Play, VR Preview, or a packaged build) to already be running before it's started.
 ** Known limitations / in progress**
- Tested primarily on **Town10HD_Opt**; moving to a different map requires re-placing the player actor and re-validating the camera height offset for that map's ground level.
- Traffic Manager pedestrian detection has been validated on **Town10HD_Opt**; a discrepancy was observed on **Town01** (vehicles not consistently detecting the player) that is still under investigation.
