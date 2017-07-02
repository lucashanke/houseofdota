(ns pipeline.pipeline
  (:use [lambdacd.steps.control-flow]
        [pipeline.steps])
  (:require
        [lambdacd.steps.manualtrigger :as manualtrigger]))

(def pipeline-def
  `(
    (either
      manualtrigger/wait-for-manual-trigger
      wait-for-repo)
    (with-workspace
      clone
      build
      (in-parallel
        run-python-unit-tests
        run-js-unit-tests
      )
      stops-linked-containers
      deploy-beat-worker
)))
