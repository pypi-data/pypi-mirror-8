/**
 * @author Manuel Guenther <Manuel.Guenther@idiap.ch>
 * @date Wed Jun  6 10:29:09 CEST 2012
 *
 * Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland
 */

#include <bob.blitz/capi.h>
#include <bob.blitz/cleanup.h>
#include <bob.io.base/api.h>

#include "ndarray.h"
#include <bob.learn.misc/BICMachine.h>

static double bic_call_(const bob::learn::misc::BICMachine& machine, bob::python::const_ndarray input){
  double o;
  machine.forward_(input.bz<double,1>(), o);
  return o;
}

static double bic_call(const bob::learn::misc::BICMachine& machine, bob::python::const_ndarray input){
  double o;
  machine.forward(input.bz<double,1>(), o);
  return o;
}

static void bic_load(bob::learn::misc::BICMachine& machine, boost::python::object file){
  if (!PyBobIoHDF5File_Check(file.ptr())) PYTHON_ERROR(TypeError, "Would have expected a bob.io.base.HDF5File");
  PyBobIoHDF5FileObject* hdf5 = (PyBobIoHDF5FileObject*) file.ptr();
  machine.load(*hdf5->f);
}

static void bic_save(const bob::learn::misc::BICMachine& machine, boost::python::object file){
  if (!PyBobIoHDF5File_Check(file.ptr())) PYTHON_ERROR(TypeError, "Would have expected a bob.io.base.HDF5File");
  PyBobIoHDF5FileObject* hdf5 = (PyBobIoHDF5FileObject*) file.ptr();
  machine.save(*hdf5->f);
}


void bind_machine_bic(){

  // bind BICMachine
  boost::python::class_<bob::learn::misc::BICMachine, boost::shared_ptr<bob::learn::misc::BICMachine> > (
      "BICMachine",
      "This machine is designed to classify image differences to be either intrapersonal or extrapersonal. "
      "There are two possible implementations of the BIC:\n"
      "\n"
      "* 'The Bayesian Intrapersonal/Extrapersonal Classifier' from Teixeira [1]_. "
      "  A full projection of the data is performed. No prior for the classes has to be selected.\n"
      "* 'Face Detection and Recognition using Maximum Likelihood Classifiers on Gabor Graphs' from Guenther and Wuertz [2]_."
      "  Only mean and variance of the difference vectors are calculated. There is no subspace truncation and no priors.\n"
      "\n"
      "What kind of machine is used is dependent on the way, this class is trained via the BICTrainer.\n"
      "\n"
      ".. [1] Marcio Luis Teixeira. The Bayesian intrapersonal/extrapersonal classifier. Colorado State University, 2003.\n"
      ".. [2] Manuel Guenther and Rolf P. Wuertz. Face detection and recognition using maximum likelihood classifiers on Gabor graphs. International Journal of Pattern Recognition and Artificial Intelligence, 23(3):433-461, 2009.",
      boost::python::init<bool>(
          (boost::python::arg("self"), boost::python::arg("use_dffs") = false),
          "Initializes an empty BICMachine. The optional boolean parameter specifies whether to use the DFFS in the BIC implementation. \n\n.. warning :: Use this flag with care, the default value 'False' is usually the best choice!"
      )
    )

    .def(
      boost::python::init<const bob::learn::misc::BICMachine&>(
          (boost::python::arg("self"), boost::python::arg("other")),
          "Constructs one BICMachine from another one by doing a deep copy."
      )
    )

    .def(
      boost::python::self == boost::python::self
    )

    .def(
      "is_similar_to",
      &bob::learn::misc::BICMachine::is_similar_to,
      (boost::python::arg("self"), boost::python::arg("other"), boost::python::arg("r_epsilon") = 1e-5, boost::python::arg("a_epsilon") = 1e-8),
      "Compares this BICMachine with the 'other' one to be approximately the same."
    )

    .def(
      "load",
      &bic_load,
      (boost::python::arg("self"), boost::python::arg("file")),
      "Loads the configuration parameters from an hdf5 file."
    )

    .def(
      "save",
      &bic_save,
      (boost::python::arg("self"), boost::python::arg("file")),
      "Saves the configuration parameters to an hdf5 file."
    )

    .def(
      "__call__",
      &bic_call,
      (
          boost::python::arg("self"),
          boost::python::arg("input")
      ),
      "Computes the BIC or IEC score for the given input vector, which results of a comparison of two (facial) images. "
      "The resulting value is returned as a single float value. "
      "The score itself is the log-likelihood score of the given input vector belonging to the intrapersonal class. "
      "No sanity checks of input and output are performed."
    )

    .def(
      "forward_",
      &bic_call_,
      (
          boost::python::arg("self"),
          boost::python::arg("input")
      ),
      "Computes the BIC or IEC score for the given input vector, which results of a comparison of two (facial) images. "
      "The score itself is the log-likelihood score of the given input vector belonging to the intrapersonal class. "
      "No sanity checks of input are performed."
    )

    .def(
      "forward",
      &bic_call,
      (
          boost::python::arg("self"),
          boost::python::arg("input")
      ),
      "Computes the BIC or IEC score for the given input vector, which results of a comparison of two (facial) images. "
      "The score itself is the log-likelihood score of the given input vector belonging to the intrapersonal class. "
      "Sanity checks of input shape are performed."
    )

    .add_property(
      "use_dffs",
      // cast overloaded function with the same name to its type...
      static_cast<bool (bob::learn::misc::BICMachine::*)() const>(&bob::learn::misc::BICMachine::use_DFFS),
      static_cast<void (bob::learn::misc::BICMachine::*)(bool)>(&bob::learn::misc::BICMachine::use_DFFS),
      "Should the Distance From Feature Space (DFFS) measure be added during scoring? \n\n.. warning :: Only set this flag to True if the number of intrapersonal and extrapersonal training pairs is approximately equal. Otherwise, weird thing may happen!"
  );
}
