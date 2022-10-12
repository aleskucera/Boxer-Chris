
(cl:in-package :asdf)

(defsystem "kinematics_6dof_ros_pkg-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "changeKinematicsConfig" :depends-on ("_package_changeKinematicsConfig"))
    (:file "_package_changeKinematicsConfig" :depends-on ("_package"))
  ))