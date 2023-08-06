# Copyright 2014 Samuel Li
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
HDFQS Python Library

This module contains the class and all functions required for reading data from HDFQS data stores.
"""

import numpy as np;
import os;
import re;
import tables;

class HDFQS:
  """
  This class wraps all functionality to read data from an HDFQS data store.
  """

################################################################################
################################# CONSTRUCTOR ##################################
################################################################################
  def __init__(self, path):
    """
    Create an HDFQS object given the path to the HDFQS data store.

    This function automatically runs :meth:`register_directory` on the HDFQS root.

    Parameters
    ----------
    path : str
      Path of root of HDFQS data store.
    """

    self.path = path;
    self.manifest_path = os.path.join(self.path, "manifest.py");
    if (os.path.exists(self.manifest_path)):
      temp = { };
      execfile(self.manifest_path, temp);
      self.manifest = temp["manifest"];
    else:
      self.manifest = { "FILES": { } };
    self.register_directory();

################################################################################
################################### REGISTER ###################################
################################################################################
  def register(self, filename):
    """
    Register a file in the HDFQS manifest.

    All HDF5 files within the HDFQS data store need to be registered in the manifest in order to be queried by HDFQS. The manifest associates all data tables with the HDF5 files that contain part of the table, along with the time range contained in each file.

    Note - all new files in the HDFQS data store are automatically registered when the HDFQS object is created. The use of this function is only required if new files are added into the HDFQS data store after the HDFQS object has been initialized.

    Parameters
    ----------
    filename : str
      Path of file to register. Can be relative to HDFQS root.
    """

    filename = os.path.join(self.path, filename); # If an absolute path is given, it does not get appended to the HDFQS path

    if (filename in self.manifest["FILES"]):
      return;

    try:
      fd = tables.openFile(filename, mode="r");
    except IOError:
      print "Error opening file %s" % ( filename );
      return;
    self.manifest["FILES"][filename] = True;
    for location in fd.root:
      for group in location:
        for table in group:
          if (type(table) != tables.Table):
            continue;
          if (table.shape == ( 0, )):
            continue;
          tm = [ x["time"] for x in table ];
          path = "/" + location._v_name + "/" + group._v_name + "/" + table.name;
          if (len(tm) > 0):
            if (not self.manifest.has_key(path)):
              self.manifest[path] = [ { "filename": filename, "start": tm[0], "stop": tm[-1] } ];
            else:
              self.manifest[path].append({ "filename": filename, "start": tm[0], "stop": tm[-1] });
    fd.close();

################################################################################
############################## REGISTER DIRECTORY ##############################
################################################################################
  def register_directory(self, path=""):
    """
    Register all HDF5 files in the specified directory.

    See documentation for :meth:`register` regarding automatic registration during initialization.

    Parameters
    ----------
    path : str
      Path of directory to register (default is the HDFQS root). Path can be relative to HDFQS root.
    """

    path = os.path.join(self.path, path);
    i = 0;
    is_hdf5 = re.compile("^.*\.h5$");
    changed = False;
    for subdir in os.listdir(path):
      if ((subdir == ".git") or (subdir == "raw") or (subdir == "manifest.py")):
        continue;
      subdir = os.path.join(path, subdir);
      if (os.path.isdir(subdir)): # Is a subdirectory
        for filename in os.listdir(subdir):
          if (not is_hdf5.match(filename)):
            i=i+1;
            continue;
          full_path = os.path.join(subdir, filename);
          if (full_path not in self.manifest["FILES"]):
            print full_path;
            self.register(full_path);
            changed = True;
      elif (is_hdf5.match(subdir)): # Is an HDF5 file in the root
        if (subdir not in self.manifest["FILES"]):
          print subdir;
          self.register(subdir);
          changed = True;

    if (changed):
      fd = open(self.manifest_path, "w");
      fd.write("manifest = " + repr(self.manifest) + "\n");
      fd.close();

################################################################################
############################### RE-REGISTER ALL ################################
################################################################################
  def reregister_all(self):
    """
    Clear the manifest and reregister all HDF5 files in HDFQS data store.

    Use of this function is generally not necessary, unless damage to the manifest file is suspected.
    """

    self.manifest = { "FILES": { } };
    self.register_directory();

################################################################################
#################################### QUERY #####################################
################################################################################
  def query(self, path, start, stop):
    """
    Return filenames containing data from the specified table and time range.

    Parameters
    ----------
    path : str
      HDF5 path to data table.
    start : int64
      Start of time range, in ns since the epoch.
    stop : int64
      End of time range, in ns since the epoch.

    Returns
    -------
    files : list
      List of filenames which contain the specified data in the specified time range.
    """

    files = [ ];
    for entry in self.manifest[path]:
      if ((entry["start"] <= stop) and (entry["stop"] >= start)):
        files.append(entry["filename"]);

    return files;

################################################################################
##################################### LOAD #####################################
################################################################################
  def load(self, path, start, stop, numpts=0, time_field="time", value_field="value"):
    """
    Return data from the specified table and time range.

    This function loads data in the HDFQS data store from the specified data table within the specified time range. Note that the time range includes the endpoints. For tables with multiple value fields (e.g. x, y, z), only a single value field may be loaded. An optional parameter can specify the number of datapoints to return, in which case the specified number of datapoints, as evenly spaced as possible within the time range, will be returned.

    Parameters
    ----------
    path : str
      HDF5 path to the data table.
    start : int64
      Start of time range, in ns since the epoch.
    stop : int64
      End of time range, in ns since the epoch.
    numpts : int
      Number of points to return. Default is 0 (return all points within the time range).
    time_field : str
      Name of the time field in the table (default is "time").
    value_field : str
      Name of the value field to load (default is "value").

    Returns
    -------
    data : numpy.ma.array
      An Nx2 array containing the requested data. The first column is the time, the second column is the value.
    """

    files = self.query(path, start, stop);
    data = None;
    for f in files:
      fd = tables.openFile(f, mode="r");
      t = fd.getNode(path);
      if (len(t) < 2):
        continue;
      if (numpts == 0): # load all points
        data_from_file = np.ma.array([ [ x[time_field], x[value_field] ] for x in fd.getNode(path).where("(%s >= %d) & (%s <= %d)" % ( time_field, start, time_field, stop )) ]);
      else:
        temp = t[0:2];
        time_res = t[1][time_field] - t[0][time_field];
        stride_time = (stop - start) / np.float64(numpts);
        stride = int(np.floor(stride_time / time_res));
        if (stride > 0):
          data_from_file = np.ma.array([ [ x[time_field], x[value_field] ] for x in fd.getNode(path).where("(%s >= %d) & (%s <= %d)" % ( time_field, start, time_field, stop ), step=stride) ]);
        else: # more pixels than datapoints in time range
          data_from_file = np.ma.array([ [ x[time_field], x[value_field] ] for x in fd.getNode(path).where("(%s >= %d) & (%s <= %d)" % ( time_field, start, time_field, stop )) ]);
      if (len(data_from_file) > 0):
        if (data is None):
          data = data_from_file;
        else:
          data = np.concatenate(( data, data_from_file ));
      fd.close();

    if (data is None):
      return np.transpose(np.ma.array([ [ ], [ ] ]));
    else:
      return data;

################################################################################
################################## GET FIELDS ##################################
################################################################################
  def get_fields(self, path):
    """
    Return all fields in a data table.

    Parameters
    ----------
    path : str
      HDF5 path to the data table.

    Returns
    -------
    fields : list
      List containing the fields of the data table.
    """

    files = self.query(path, 0, np.Inf);
    if (len(files) == 0):
      raise Exception("Nonexistant path: \"%s\"" % path);
    else:
      filename = files[0];
      fd = tables.openFile(filename);
      table = fd.getNode(path);
      fields = table.colnames;
      fd.close();
      return fields;

################################################################################
#################################### CLEAN #####################################
################################################################################
  def sanitize(self, filename, min_time=31536000000000000L, index=True):
    """
    Sanitize all tables in specified file.

    For each table in the file, this function removes all data entries with an invalid time (any time before the specified minimum time), and optionally adds a completely-sorted index on the time column (to speed up loading data).

    Parameters
    ----------
    filename : str
      Name of HDF5 file (absolute or relative to HDFQS root).
    min_time : int64
      Earliest valid time, in ns since the epoch (default is 1/1/1971 00:00:00 UTC).
    index : bool
      Whether or not to create a completely-sorted index on the time column (default is True).
    """

    filename = os.path.join(self.path, filename);
    fd = tables.openFile(filename, mode="a");
    print filename;

    g = fd.root;
    for loc in g._v_children.items():
      loc = loc[1];
      for cat in loc._v_children.items():
        cat = cat[1];
        for t in cat._v_children.items():
          t = t[1];

          # Check if table is empty
          if (t.shape == ( 0, )):
            print "0%s" % ( t.name );
            continue;

          # Check for time before minimum
          bad_rows = t.read_where("time < min_time", { "min_time": min_time });
          if (bad_rows.shape[0] > 0):
            x = "-%s,%d" % ( t.name, t.shape[0] );
            tname = t.name;
            tnew = fd.createTable(cat, "%s_new" % ( tname ), t.description, t.title, filters=t.filters);
            t.attrs._f_copy(tnew);
            t.append_where(tnew, "time >= min_time", { "min_time": min_time });
            tnew.flush();
            t.remove();
            tnew.move(None, tname);
            x = "%s,%d,%d" % ( x, tnew.shape[0], bad_rows.shape[0] );
            print x;
            t = tnew;

          # Check if table is empty
          if (t.shape == ( 0, )):
            print "0%s" % ( t.name );
            continue;

          # Check for existance of time index
          if (index and (not t.cols.time.is_indexed)):
            print "*%s" % ( t.name );
            t.cols.time.create_csindex();

    fd.close();

################################################################################
############################### CLEAN DIRECTORY ################################
################################################################################
  def sanitize_directory(self, path, no_links=False, min_time=31536000000000000L, index=True):
    """
    Sanitize all files in the specified directory.
    
    Run :meth:`sanitize` on all HDF5 files in the specified directory, recursing through all subdirectories. Links may be optionally ignored, for use with git annex. In this case, all files added into git annex can be assumed to be sanitized, while files not yet added (or which have been unlocked) will be sanitized.

    Parameters
    ----------
    path : str
      Path of directory to sanitize.
    no_links : bool
      Whether or not to ignore symlinks (default is False).
    min_time : int64
      Earliest valid time, in ns since the epoch (default is 1/1/1971 00:00:00 UTC).
    index : bool
      Whether or not to create a completed-sorted index on the time column (Default is False).
    """

    path = os.path.join(self.path, path);
    if (not os.path.exists(path)):
      print("Invalid path - \"%s\"" % ( path ));
      return;
    for filename in os.listdir(path):
      if ((filename == ".git") or (filename == "raw")):
        continue;

      full_path = os.path.join(path, filename);
      if (os.path.isdir(full_path)):
        self.sanitize_directory(full_path, min_time=min_time, index=index);
      elif (no_links and os.path.islink(full_path)):
        continue;
      elif (filename[-3:] == ".h5"):
        self.sanitize(full_path, min_time=min_time, index=index);

