(defproject pipeline "0.1.0-SNAPSHOT"
            :description "FIXME: write description"
            :url "http://example.com/FIXME"
            :dependencies [[lambdacd "0.13.2"]
                           [lambdaui "0.4.0"]
                           [http-kit "2.2.0"]
                           [lambdacd-git "0.2.0"]
                           [org.clojure/clojure "1.7.0"]
                           [org.clojure/tools.logging "0.3.1"]
                           [org.slf4j/slf4j-api "1.7.5"]
                           [ch.qos.logback/logback-core "1.0.13"]
                           [ch.qos.logback/logback-classic "1.0.13"]]
            :profiles {:uberjar {:aot :all}}
            :main pipeline.core)
