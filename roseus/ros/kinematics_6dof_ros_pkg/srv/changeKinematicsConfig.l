;; Auto-generated. Do not edit!


(when (boundp 'kinematics_6dof_ros_pkg::changeKinematicsConfig)
  (if (not (find-package "KINEMATICS_6DOF_ROS_PKG"))
    (make-package "KINEMATICS_6DOF_ROS_PKG"))
  (shadow 'changeKinematicsConfig (find-package "KINEMATICS_6DOF_ROS_PKG")))
(unless (find-package "KINEMATICS_6DOF_ROS_PKG::CHANGEKINEMATICSCONFIG")
  (make-package "KINEMATICS_6DOF_ROS_PKG::CHANGEKINEMATICSCONFIG"))
(unless (find-package "KINEMATICS_6DOF_ROS_PKG::CHANGEKINEMATICSCONFIGREQUEST")
  (make-package "KINEMATICS_6DOF_ROS_PKG::CHANGEKINEMATICSCONFIGREQUEST"))
(unless (find-package "KINEMATICS_6DOF_ROS_PKG::CHANGEKINEMATICSCONFIGRESPONSE")
  (make-package "KINEMATICS_6DOF_ROS_PKG::CHANGEKINEMATICSCONFIGRESPONSE"))

(in-package "ROS")





(defclass kinematics_6dof_ros_pkg::changeKinematicsConfigRequest
  :super ros::object
  :slots (_configuration _eef_robot_frame ))

(defmethod kinematics_6dof_ros_pkg::changeKinematicsConfigRequest
  (:init
   (&key
    ((:configuration __configuration) "")
    ((:eef_robot_frame __eef_robot_frame) "")
    )
   (send-super :init)
   (setq _configuration (string __configuration))
   (setq _eef_robot_frame (string __eef_robot_frame))
   self)
  (:configuration
   (&optional __configuration)
   (if __configuration (setq _configuration __configuration)) _configuration)
  (:eef_robot_frame
   (&optional __eef_robot_frame)
   (if __eef_robot_frame (setq _eef_robot_frame __eef_robot_frame)) _eef_robot_frame)
  (:serialization-length
   ()
   (+
    ;; string _configuration
    4 (length _configuration)
    ;; string _eef_robot_frame
    4 (length _eef_robot_frame)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _configuration
       (write-long (length _configuration) s) (princ _configuration s)
     ;; string _eef_robot_frame
       (write-long (length _eef_robot_frame) s) (princ _eef_robot_frame s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _configuration
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _configuration (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _eef_robot_frame
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _eef_robot_frame (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass kinematics_6dof_ros_pkg::changeKinematicsConfigResponse
  :super ros::object
  :slots (_result ))

(defmethod kinematics_6dof_ros_pkg::changeKinematicsConfigResponse
  (:init
   (&key
    ((:result __result) "")
    )
   (send-super :init)
   (setq _result (string __result))
   self)
  (:result
   (&optional __result)
   (if __result (setq _result __result)) _result)
  (:serialization-length
   ()
   (+
    ;; string _result
    4 (length _result)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _result
       (write-long (length _result) s) (princ _result s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _result
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _result (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass kinematics_6dof_ros_pkg::changeKinematicsConfig
  :super ros::object
  :slots ())

(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfig :md5sum-) "f5f869dd94ca439f0a9ec55af2a70f63")
(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfig :datatype-) "kinematics_6dof_ros_pkg/changeKinematicsConfig")
(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfig :request) kinematics_6dof_ros_pkg::changeKinematicsConfigRequest)
(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfig :response) kinematics_6dof_ros_pkg::changeKinematicsConfigResponse)

(defmethod kinematics_6dof_ros_pkg::changeKinematicsConfigRequest
  (:response () (instance kinematics_6dof_ros_pkg::changeKinematicsConfigResponse :init)))

(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfigRequest :md5sum-) "f5f869dd94ca439f0a9ec55af2a70f63")
(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfigRequest :datatype-) "kinematics_6dof_ros_pkg/changeKinematicsConfigRequest")
(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfigRequest :definition-)
      "string configuration
string eef_robot_frame
---
string result

")

(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfigResponse :md5sum-) "f5f869dd94ca439f0a9ec55af2a70f63")
(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfigResponse :datatype-) "kinematics_6dof_ros_pkg/changeKinematicsConfigResponse")
(setf (get kinematics_6dof_ros_pkg::changeKinematicsConfigResponse :definition-)
      "string configuration
string eef_robot_frame
---
string result

")



(provide :kinematics_6dof_ros_pkg/changeKinematicsConfig "f5f869dd94ca439f0a9ec55af2a70f63")


