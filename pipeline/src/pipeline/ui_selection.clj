(ns pipeline.ui-selection
  (:require
    [hiccup.core :as h]
    [lambdaui.core :as lambdaui]
    [lambdacd.ui.core :as reference-ui]
    [compojure.core :refer [routes GET context]])
  (:gen-class))

(defn- ui-selection []
  (h/html
    [:html
     [:head
      [:title "LambdaCD - UI Selection"]]
     [:body
      [:h1 "LambdaCD - UI Selection"]
      [:p "Two different UIs for LambdaCD exist: The reference-ui shipped with the core of LambdaCD and "
       [:a {:href "https://github.com/sroidl/lambda-ui"} "LambdaUI"]
       ", a community developed, opinionated alternative with a more user friendly interface"]
      [:ul
       [:li [:a {:href "./lambdaui/lambdaui/index.html"} "LambdaUI"]]
       [:li [:a {:href "./reference/"} "Reference UI"]]]]]))

(defn ui-routes [pipeline]
  (let [lambdaui-app    (lambdaui/ui-for pipeline :contextPath "/lambdaui")
        referenceui-app (reference-ui/ui-for pipeline)]
    (routes
      (GET "/" [] (ui-selection))
      (context "/lambdaui"  [] lambdaui-app)
      (context "/reference" [] referenceui-app))))

