/**
 * @file trainer/python/bic.cc
 * @date Wed Jun  6 10:29:09 CEST 2012
 * @author Manuel Guenther <Manuel.Guenther@idiap.ch>
 *
 * Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
 */

#include "ndarray.h"
#include <bob.learn.misc/BICTrainer.h>

void py_train(const bob::learn::misc::BICTrainer& t,
  bob::learn::misc::BICMachine& m, bob::python::const_ndarray intra_differences,
  bob::python::const_ndarray extra_differences)
{
  t.train(m, intra_differences.bz<double,2>(),
    extra_differences.bz<double,2>());
}



void bind_trainer_bic(){

  boost::python::class_<bob::learn::misc::BICTrainer, boost::shared_ptr<bob::learn::misc::BICTrainer> > (
      "BICTrainer",
      "A Trainer for a BICMachine. It trains either a BIC model (including projection matrix and eigenvalues), "
          "or an IEC model (containing mean and variance only). See :py:class:`bob.machine.BICMachine` for more details.",
      boost::python::init<int,int>(
          (
              boost::python::arg("self"),
              boost::python::arg("intra_dim"),
              boost::python::arg("extra_dim")
          ),
          "Initializes the BICTrainer to train a BIC model with the given resulting dimensions of the intraperonal and extrapersonal subspaces."
      )
    )

    .def(
      boost::python::init<>(
        (boost::python::arg("self")),
        "Initializes the BICTrainer to train a IEC model."
      )
    )

    .def(
      "train",
      &py_train,
      (
          boost::python::arg("self"),
          boost::python::arg("machine"),
          boost::python::arg("intra_differences"),
          boost::python::arg("extra_differences")
      ),
      "Trains the given machine (should be of type :py:class:`bob.machine.BICMachine`) to classify intrapersonal image differences vs. extrapersonal ones. "
      "The given difference vectors might be the result of any image comparison function, e.g., the pixel difference of the images."
    );
}
