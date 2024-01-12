# .gitpod.Dockerfile

FROM gitpod/workspace-full:latest

# Install libGL.so.1
RUN sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx
