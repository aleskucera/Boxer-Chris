; Auto-generated. Do not edit!


(cl:in-package papouch_ros-srv)


;//! \htmlinclude WriteIO-request.msg.html

(cl:defclass <WriteIO-request> (roslisp-msg-protocol:ros-message)
  ((channel
    :reader channel
    :initarg :channel
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0))
   (state
    :reader state
    :initarg :state
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0)))
)

(cl:defclass WriteIO-request (<WriteIO-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <WriteIO-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'WriteIO-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name papouch_ros-srv:<WriteIO-request> is deprecated: use papouch_ros-srv:WriteIO-request instead.")))

(cl:ensure-generic-function 'channel-val :lambda-list '(m))
(cl:defmethod channel-val ((m <WriteIO-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader papouch_ros-srv:channel-val is deprecated.  Use papouch_ros-srv:channel instead.")
  (channel m))

(cl:ensure-generic-function 'state-val :lambda-list '(m))
(cl:defmethod state-val ((m <WriteIO-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader papouch_ros-srv:state-val is deprecated.  Use papouch_ros-srv:state instead.")
  (state m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <WriteIO-request>) ostream)
  "Serializes a message object of type '<WriteIO-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'channel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    ))
   (cl:slot-value msg 'channel))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'state))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    ))
   (cl:slot-value msg 'state))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <WriteIO-request>) istream)
  "Deserializes a message object of type '<WriteIO-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'channel) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'channel)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256)))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'state) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'state)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256)))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<WriteIO-request>)))
  "Returns string type for a service object of type '<WriteIO-request>"
  "papouch_ros/WriteIORequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WriteIO-request)))
  "Returns string type for a service object of type 'WriteIO-request"
  "papouch_ros/WriteIORequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<WriteIO-request>)))
  "Returns md5sum for a message object of type '<WriteIO-request>"
  "acedff32d14bc005248c00858b1d9393")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'WriteIO-request)))
  "Returns md5sum for a message object of type 'WriteIO-request"
  "acedff32d14bc005248c00858b1d9393")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<WriteIO-request>)))
  "Returns full string definition for message of type '<WriteIO-request>"
  (cl:format cl:nil "~%# List of IO channels to write.~%int8[] channel~%~%# List of state~%int8[] state~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'WriteIO-request)))
  "Returns full string definition for message of type 'WriteIO-request"
  (cl:format cl:nil "~%# List of IO channels to write.~%int8[] channel~%~%# List of state~%int8[] state~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <WriteIO-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'channel) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'state) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <WriteIO-request>))
  "Converts a ROS message object to a list"
  (cl:list 'WriteIO-request
    (cl:cons ':channel (channel msg))
    (cl:cons ':state (state msg))
))
;//! \htmlinclude WriteIO-response.msg.html

(cl:defclass <WriteIO-response> (roslisp-msg-protocol:ros-message)
  ((retval
    :reader retval
    :initarg :retval
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass WriteIO-response (<WriteIO-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <WriteIO-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'WriteIO-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name papouch_ros-srv:<WriteIO-response> is deprecated: use papouch_ros-srv:WriteIO-response instead.")))

(cl:ensure-generic-function 'retval-val :lambda-list '(m))
(cl:defmethod retval-val ((m <WriteIO-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader papouch_ros-srv:retval-val is deprecated.  Use papouch_ros-srv:retval instead.")
  (retval m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <WriteIO-response>) ostream)
  "Serializes a message object of type '<WriteIO-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'retval) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <WriteIO-response>) istream)
  "Deserializes a message object of type '<WriteIO-response>"
    (cl:setf (cl:slot-value msg 'retval) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<WriteIO-response>)))
  "Returns string type for a service object of type '<WriteIO-response>"
  "papouch_ros/WriteIOResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WriteIO-response)))
  "Returns string type for a service object of type 'WriteIO-response"
  "papouch_ros/WriteIOResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<WriteIO-response>)))
  "Returns md5sum for a message object of type '<WriteIO-response>"
  "acedff32d14bc005248c00858b1d9393")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'WriteIO-response)))
  "Returns md5sum for a message object of type 'WriteIO-response"
  "acedff32d14bc005248c00858b1d9393")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<WriteIO-response>)))
  "Returns full string definition for message of type '<WriteIO-response>"
  (cl:format cl:nil "bool retval~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'WriteIO-response)))
  "Returns full string definition for message of type 'WriteIO-response"
  (cl:format cl:nil "bool retval~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <WriteIO-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <WriteIO-response>))
  "Converts a ROS message object to a list"
  (cl:list 'WriteIO-response
    (cl:cons ':retval (retval msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'WriteIO)))
  'WriteIO-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'WriteIO)))
  'WriteIO-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WriteIO)))
  "Returns string type for a service object of type '<WriteIO>"
  "papouch_ros/WriteIO")