(ns pipeline.steps
  (:require [lambdacd.steps.shell :as shell]
            [lambdacd-git.core :as lambdacd-git]))

(def repo-uri "https://github.com/lucashanke/houseofdota.git")
(def repo-branch "master-beatworker")
(ns pipeline.steps
  (:require [lambdacd.steps.shell :as shell]))

(defn wait-for-repo [args ctx]
(lambdacd-git/wait-for-git ctx repo-uri :ref (str "refs/heads/" repo-branch)))

(defn clone [args ctx]
  (let [revision (:revision args)
        cwd      (:cwd args)
        ref      (or revision repo-branch)]
    (lambdacd-git/clone ctx repo-uri ref cwd)))

(defn build [args ctx]
  (shell/bash ctx (:cwd args) "docker-compose build"))

(defn migrate-db [args ctx]
  (shell/bash ctx (:cwd args) "docker-compose -p houseofdota up --abort-on-container-exit db_migrate"))

(defn deploy-beat-worker [args ctx]
  (shell/bash ctx (:cwd args) "docker-compose -p houseofdota up -d --force-recreate beat worker"))
