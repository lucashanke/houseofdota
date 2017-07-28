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
      migrate-db
      deploy-beat-worker
)))
