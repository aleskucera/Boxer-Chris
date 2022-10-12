
(cl:in-package :asdf)

(defsystem "papouch_ros-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "WriteIO" :depends-on ("_package_WriteIO"))
    (:file "_package_WriteIO" :depends-on ("_package"))
  ))