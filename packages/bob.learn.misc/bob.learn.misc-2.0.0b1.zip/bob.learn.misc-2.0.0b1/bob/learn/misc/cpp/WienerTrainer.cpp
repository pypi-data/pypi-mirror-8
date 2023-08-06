/**
 * @date Fri Sep 30 16:58:42 2011 +0200
 * @author Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
 *
 * Copyright (C) Idiap Research Institute, Martigny, Switzerland
 */

#include <bob.learn.misc/WienerTrainer.h>
#include <bob.core/cast.h>
#include <bob.sp/FFT2D.h>
#include <complex>

bob::learn::misc::WienerTrainer::WienerTrainer()
{
}

bob::learn::misc::WienerTrainer::WienerTrainer(const bob::learn::misc::WienerTrainer& other)
{
}

bob::learn::misc::WienerTrainer::~WienerTrainer()
{
}

bob::learn::misc::WienerTrainer& bob::learn::misc::WienerTrainer::operator=
(const bob::learn::misc::WienerTrainer& other)
{
  return *this;
}

bool bob::learn::misc::WienerTrainer::operator==
  (const bob::learn::misc::WienerTrainer& other) const
{
  return true;
}

bool bob::learn::misc::WienerTrainer::operator!=
  (const bob::learn::misc::WienerTrainer& other) const
{
  return !(this->operator==(other));
}

bool bob::learn::misc::WienerTrainer::is_similar_to
  (const bob::learn::misc::WienerTrainer& other, const double r_epsilon,
   const double a_epsilon) const
{
  return true;
}

void bob::learn::misc::WienerTrainer::train(bob::learn::misc::WienerMachine& machine,
    const blitz::Array<double,3>& ar)
{
  // Data is checked now and conforms, just proceed w/o any further checks.
  const size_t n_samples = ar.extent(0);
  const size_t height = ar.extent(1);
  const size_t width = ar.extent(2);
  // machine dimensions
  const size_t height_m = machine.getHeight();
  const size_t width_m = machine.getWidth();

  // Checks that the dimensions are matching
  if (height != height_m) {
    boost::format m("number of inputs (height) for machine (%u) does not match number of columns at input parameter (%u)");
    m % height_m % height;
    throw std::runtime_error(m.str());
  }
  if (width != width_m) {
    boost::format m("number of inputs (width) for machine (%u) does not match number of depths at input parameter (%u)");
    m % width_m % width;
    throw std::runtime_error(m.str());
  }

  // FFT2D
  bob::sp::FFT2D fft2d(height, width);

  // Loads the data
  blitz::Array<double,3> data(height, width, n_samples);
  blitz::Array<std::complex<double>,2> sample_fft(height, width);
  blitz::Range all = blitz::Range::all();
  for (size_t i=0; i<n_samples; ++i) {
    blitz::Array<double,2> sample = ar(i,all,all);
    blitz::Array<std::complex<double>,2> sample_c = bob::core::array::cast<std::complex<double> >(sample);
    fft2d(sample_c, sample_fft);
    data(all,all,i) = blitz::abs(sample_fft);
  }
  // Computes the mean of the training data
  blitz::Array<double,2> tmp(height,width);
  blitz::thirdIndex k;
  tmp = blitz::mean(data,k);
  // Removes the mean from the data
  for (size_t i=0; i<n_samples; ++i) {
    data(all,all,i) -= tmp;
  }
  // Computes power of 2 values
  data *= data;
  // Sums to get the variance
  tmp = blitz::sum(data,k) / n_samples;

  // sets the Wiener machine with the results:
  machine.setPs(tmp);
}
