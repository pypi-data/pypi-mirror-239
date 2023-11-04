// Document need to be synced with `README.md` manually.
//! # Fast Event Voxel Builder
//! [\[Codeberg Repo\]](https://codeberg.org/ybh1998/EventVoxelBuilder/)
//! [\[API Document\]](https://ybh1998.codeberg.page/EventVoxelBuilder/)
//!
//! ### Warning: Very Unstable API!
//! This is currently a rush project for CVPR 2024 and the API will definitely be rewritten after the DDL.
//!
//! ### To run the example Python codes or your own Python code
//! 1. Download `event-voxel-builder-*.whl` under [\[releases\]](https://codeberg.org/ybh1998/LibreDR/releases/) and \
//! install using `pip install`, or install from [\[PyPI\]](https://pypi.org/project/libredr/).
//! 2. Run Python example codes in `examples` or your own codes.
//!
//! Copyright (c) 2023 Bohan Yu. All rights reserved. \
//! EventVoxelBuilder is free software licensed under GNU Affero General Public License version 3 or latter.

use std::env;
use std::marker::{Send, Sync};
use tracing::warn;
use itertools::izip;
use pyo3::prelude::*;
use rayon::prelude::*;
use shadow_rs::shadow;
use ndarray::prelude::*;
use anyhow::{Result, ensure};
use num_traits::int::PrimInt;
use numpy::{PyReadonlyArray1, PyArray3, ToPyArray};
use tracing_subscriber::{fmt, EnvFilter, prelude::*};

shadow!(build);

struct EventVoxelBuilder {
  n_time: u64,
  n_row: u16,
  n_col: u16,
  timestamp_per_time: u64,
  pool: rayon::ThreadPool,
  sort_axis: usize,
}

impl EventVoxelBuilder {
  /// * `n_time`, `n_row`, `n_col` - The shape of returned voxel.
  /// * `timestamp_per_time` - Gather all events within `timestamp_per_time` into one time slice.
  /// * `num_threads` - Number of threads. If `num_threads` is 0, select automatically. Default: 0.
  /// * `sort_axis` - Along which axis to split events for parallel processing.
  ///                 `0` for `i_time`, `1` for `i_row`, `2` for `i_col`. Default: 0.
  fn new(
      n_time: u64,
      n_row: u16,
      n_col: u16,
      timestamp_per_time: u64,
      num_threads: Option<usize>,
      sort_axis: Option<usize>) -> Result<Self> {
    let sort_axis = sort_axis.unwrap_or(0);
    ensure!(sort_axis < 3);
    Ok(EventVoxelBuilder {
      n_time,
      n_row,
      n_col,
      timestamp_per_time,
      pool: rayon::ThreadPoolBuilder::new().num_threads(num_threads.unwrap_or(0)).build()?,
      sort_axis,
    })
  }

  fn build<T: PrimInt + std::ops::AddAssign + std::convert::From<i8> + Send + Sync>(
      &self,
      timestamps: &[u64],
      i_row: &[u16],
      i_col: &[u16],
      polarity: &[i8]) -> Result<Array3<T>> {
    let n_events = timestamps.len();
    ensure!(polarity.len() == n_events);
    ensure!(i_row.len() == n_events);
    ensure!(i_col.len() == n_events);
    let events = self.pool.install(|| {
      let mut events: Vec<_> = izip!(timestamps, i_row, i_col, polarity).filter(|event| {
        *event.0 < self.n_time * self.timestamp_per_time &&
          *event.1 < self.n_row &&
          *event.2 < self.n_col &&
          (*event.3 == 1 || *event.3 == (-1).into())
      }).collect();
      if events.len() < n_events {
        warn!("EventVoxelBuilder::build: {} events filterred from {}.", n_events - events.len(), n_events);
      }
      match self.sort_axis {
        0 => events.par_sort_unstable_by_key(|e| e.0 / self.timestamp_per_time),
        1 => events.par_sort_unstable_by_key(|e| e.1),
        2 => events.par_sort_unstable_by_key(|e| e.2),
        _ => unreachable!(),
      };
      events
    });
    let mut voxel = Array3::zeros((self.n_time as usize, self.n_row as usize, self.n_col as usize));
    let mut idx = Array1::zeros(voxel.shape()[self.sort_axis] + 1);
    *idx.last_mut().unwrap() = events.len();
    let mut curr_idx = 1;
    for (i, event) in events.iter().enumerate() {
      let curr_event_idx = match self.sort_axis {
        0 => (event.0 / self.timestamp_per_time) as usize,
        1 => *event.1 as usize,
        2 => *event.2 as usize,
        _ => unreachable!(),
      };
      while curr_idx < idx.len() && curr_event_idx  + 1 > curr_idx {
        idx[curr_idx] = i;
        curr_idx += 1;
      }
    }
    self.pool.install(|| {
      voxel.axis_iter_mut(Axis(self.sort_axis)).into_par_iter().enumerate().for_each(|(i, mut voxel)| {
        for event in &events[idx[i]..idx[i + 1]] {
          match self.sort_axis {
            0 => {
              voxel[[*event.1 as usize, *event.2 as usize]] += (*event.3).into();
            },
            1 => todo!(),
            2 => todo!(),
            _ => unreachable!(),
          };
        }
      });
    });
    Ok(voxel)
  }
}

#[pyclass(name = "EventVoxelBuilder")]
struct PyEventVoxelBuilder {
  event_voxel_builder: EventVoxelBuilder,
}

#[pymethods]
impl PyEventVoxelBuilder {
  #[new]
  fn py_new(
      n_time: u64,
      n_row: u16,
      n_col: u16,
      timestamp_per_time: u64,
      num_threads: Option<usize>,
      sort_axis: Option<usize>) -> Result<Self> {
    Ok(PyEventVoxelBuilder {
      event_voxel_builder: EventVoxelBuilder::new(n_time, n_row, n_col, timestamp_per_time, num_threads, sort_axis)?,
    })
  }

  #[pyo3(name = "build")]
  fn py_build(
      &self,
      py: Python,
      timestamps: PyReadonlyArray1<u64>,
      i_row: PyReadonlyArray1<u16>,
      i_col: PyReadonlyArray1<u16>,
      polarity: PyReadonlyArray1<i8>) -> Result<Py<PyArray3<i32>>> {
    let timestamps = timestamps.as_slice()?;
    let i_row = i_row.as_slice()?;
    let i_col = i_col.as_slice()?;
    let polarity = polarity.as_slice()?;
    let voxel = py.allow_threads(|| {
      self.event_voxel_builder.build(timestamps, i_row, i_col, polarity)
    })?;
    Ok(voxel.to_pyarray(py).to_owned())
  }
}

fn init_static() -> Result<()> {
  let log_level = env::var("EVENT_VOXEL_BUILDER_LOG_LEVEL").unwrap_or(String::from("info"));
  let filter_layer = EnvFilter::try_new(log_level)?;
  let fmt_layer = fmt::layer()
    .with_target(false);
  tracing_subscriber::registry()
    .with(filter_layer)
    .with(fmt_layer)
    .init();
  Ok(())
}

/// Initialize Python module.
///
/// Accept `EVENT_VOXEL_BUILDER_LOG_LEVEL` environment variable to set `log_level`.
/// * (default: info, feasible: debug, info, warn, error)
#[pymodule]
#[pyo3(name = "event_voxel_builder")]
pub fn py_event_voxel_builder(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
  init_static()?;
  module.add("__author__", "Bohan Yu <ybh1998@protonmail.com>")?;
  module.add("__version__", format!("EventVoxelBuilder {}", build::PKG_VERSION))?;
  module.add_class::<PyEventVoxelBuilder>()?;
  Ok(())
}
