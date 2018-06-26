# docker build -t jupyterlab_geojs .
# docker run -it --rm -p 7227:7227 --hostname localhost jupyterlab_geojs
# Find the URL in the console and open browser to that url

# You must first build the thirdparty image, which is at
# project/docker/thirdparty/Dockerfile
# (docker build -t jupyterlab_geojs/thirdparty project/docker/thirdparty)
FROM jupyterlab_geojs/thirdparty

# Copy source files
ADD ./ /home/$NB_USER/jupyterlab_geojs

# Must be root user to install extension
USER root

# Install JupyterLab extension
WORKDIR /home/$NB_USER/jupyterlab_geojs
RUN python setup.py install
RUN jupyter labextension install .

# Must also be root user at runtime to bypass error messages
#USER $NB_USER

# Setup entry point
WORKDIR /home/$NB_USER/jupyterlab_geojs/notebooks
EXPOSE 7227
ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--port=7227", "--allow-root", "--no-browser"]
