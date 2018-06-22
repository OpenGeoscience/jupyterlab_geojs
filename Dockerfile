# docker build -t lab_geojs .
# docker run -it --rm -p 7227:7227 --hostname localhost lab_geojs
# Find the URL in the console and open browser to that url

# Per jupyter docker-stacks:
# https://github.com/jupyter/docker-stacks/tree/master/base-notebook
# http://jupyter-docker-stacks.readthedocs.io/en/latest/index.html
FROM jupyter/base-notebook

# Install jupyterlab widget manager (needed for custom widgets)
# For some reason, must install this *before* local extension
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager

# Copy files under user's directory
WORKDIR /home/$NB_USER/work/hack
ADD ./ ./

# Install python requirements (GDAL et al)
RUN conda install --yes --file requirements.txt

# Install extension -- must do this as root user
USER root
RUN python setup.py install
RUN jupyter labextension install .
USER $NB_USER

# Setup entry point
WORKDIR /home/$NB_USER/work/hack/notebooks
EXPOSE 7227
ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--port=7227", "--allow-root", "--no-browser"]
