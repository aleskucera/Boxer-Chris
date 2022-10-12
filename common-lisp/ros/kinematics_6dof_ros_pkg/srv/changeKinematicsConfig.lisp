; Auto-generated. Do not edit!


(cl:in-package kinematics_6dof_ros_pkg-srv)


;//! \htmlinclude changeKinematicsConfig-request.msg.html

(cl:defclass <changeKinematicsConfig-request> (roslisp-msg-protocol:ros-message)
  ((configuration
    :reader configuration
    :initarg :configuration
    :type cl:string
    :initform "")
   (eef_robot_frame
    :reader eef_robot_frame
    :initarg :eef_robot_frame
    :type cl:string
    :initform ""))
)

(cl:defclass changeKinematicsConfig-request (<changeKinematicsConfig-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeKinematicsConfig-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeKinematicsConfig-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kinematics_6dof_ros_pkg-srv:<changeKinematicsConfig-request> is deprecated: use kinematics_6dof_ros_pkg-srv:changeKinematicsConfig-request instead.")))

(cl:ensure-generic-function 'configuration-val :lambda-list '(m))
(cl:defmethod configuration-val ((m <changeKinematicsConfig-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kinematics_6dof_ros_pkg-srv:configuration-val is deprecated.  Use kinematics_6dof_ros_pkg-srv:configuration instead.")
  (configuration m))

(cl:ensure-generic-function 'eef_robot_frame-val :lambda-list '(m))
(cl:defmethod eef_robot_frame-val ((m <changeKinematicsConfig-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kinematics_6dof_ros_pkg-srv:eef_robot_frame-val is deprecated.  Use kinematics_6dof_ros_pkg-srv:eef_robot_frame instead.")
  (eef_robot_frame m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeKinematicsConfig-request>) ostream)
  "Serializes a message object of type '<changeKinematicsConfig-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'configuration))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'configuration))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'eef_robot_frame))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'eef_robot_frame))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeKinematicsConfig-request>) istream)
  "Deserializes a message object of type '<changeKinematicsConfig-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'configuration) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'configuration) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'eef_robot_frame) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'eef_robot_frame) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeKinematicsConfig-request>)))
  "Returns string type for a service object of type '<changeKinematicsConfig-request>"
  "kinematics_6dof_ros_pkg/changeKinematicsConfigRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeKinematicsConfig-request)))
  "Returns string type for a service object of type 'changeKinematicsConfig-request"
  "kinematics_6dof_ros_pkg/changeKinematicsConfigRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeKinematicsConfig-request>)))
  "Returns md5sum for a message object of type '<changeKinematicsConfig-request>"
  "f5f869dd94ca439f0a9ec55af2a70f63")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeKinematicsConfig-request)))
  "Returns md5sum for a message object of type 'changeKinematicsConfig-request"
  "f5f869dd94ca439f0a9ec55af2a70f63")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeKinematicsConfig-request>)))
  "Returns full string definition for message of type '<changeKinematicsConfig-request>"
  (cl:format cl:nil "string configuration~%string eef_robot_frame~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeKinematicsConfig-request)))
  "Returns full string definition for message of type 'changeKinematicsConfig-request"
  (cl:format cl:nil "string configuration~%string eef_robot_frame~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeKinematicsConfig-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'configuration))
     4 (cl:length (cl:slot-value msg 'eef_robot_frame))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeKinematicsConfig-request>))
  "Converts a ROS message object to a list"
  (cl:list 'changeKinematicsConfig-request
    (cl:cons ':configuration (configuration msg))
    (cl:cons ':eef_robot_frame (eef_robot_frame msg))
))
;//! \htmlinclude changeKinematicsConfig-response.msg.html

(cl:defclass <changeKinematicsConfig-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:string
    :initform ""))
)

(cl:defclass changeKinematicsConfig-response (<changeKinematicsConfig-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeKinematicsConfig-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeKinematicsConfig-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kinematics_6dof_ros_pkg-srv:<changeKinematicsConfig-response> is deprecated: use kinematics_6dof_ros_pkg-srv:changeKinematicsConfig-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <changeKinematicsConfig-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kinematics_6dof_ros_pkg-srv:result-val is deprecated.  Use kinematics_6dof_ros_pkg-srv:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeKinematicsConfig-response>) ostream)
  "Serializes a message object of type '<changeKinematicsConfig-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'result))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'result))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeKinematicsConfig-response>) istream)
  "Deserializes a message object of type '<changeKinematicsConfig-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'result) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'result) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeKinematicsConfig-response>)))
  "Returns string type for a service object of type '<changeKinematicsConfig-response>"
  "kinematics_6dof_ros_pkg/changeKinematicsConfigResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeKinematicsConfig-response)))
  "Returns string type for a service object of type 'changeKinematicsConfig-response"
  "kinematics_6dof_ros_pkg/changeKinematicsConfigResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeKinematicsConfig-response>)))
  "Returns md5sum for a message object of type '<changeKinematicsConfig-response>"
  "f5f869dd94ca439f0a9ec55af2a70f63")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeKinematicsConfig-response)))
  "Returns md5sum for a message object of type 'changeKinematicsConfig-response"
  "f5f869dd94ca439f0a9ec55af2a70f63")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeKinematicsConfig-response>)))
  "Returns full string definition for message of type '<changeKinematicsConfig-response>"
  (cl:format cl:nil "string result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeKinematicsConfig-response)))
  "Returns full string definition for message of type 'changeKinematicsConfig-response"
  (cl:format cl:nil "string result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeKinematicsConfig-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'result))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeKinematicsConfig-response>))
  "Converts a ROS message object to a list"
  (cl:list 'changeKinematicsConfig-response
    (cl:cons ':result (result msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'changeKinematicsConfig)))
  'changeKinematicsConfig-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'changeKinematicsConfig)))
  'changeKinematicsConfig-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeKinematicsConfig)))
  "Returns string type for a service object of type '<changeKinematicsConfig>"
  "kinematics_6dof_ros_pkg/changeKinematicsConfig")