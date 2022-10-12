;; Auto-generated. Do not edit!


(when (boundp 'papouch_ros::WriteIO)
  (if (not (find-package "PAPOUCH_ROS"))
    (make-package "PAPOUCH_ROS"))
  (shadow 'WriteIO (find-package "PAPOUCH_ROS")))
(unless (find-package "PAPOUCH_ROS::WRITEIO")
  (make-package "PAPOUCH_ROS::WRITEIO"))
(unless (find-package "PAPOUCH_ROS::WRITEIOREQUEST")
  (make-package "PAPOUCH_ROS::WRITEIOREQUEST"))
(unless (find-package "PAPOUCH_ROS::WRITEIORESPONSE")
  (make-package "PAPOUCH_ROS::WRITEIORESPONSE"))

(in-package "ROS")





(defclass papouch_ros::WriteIORequest
  :super ros::object
  :slots (_channel _state ))

(defmethod papouch_ros::WriteIORequest
  (:init
   (&key
    ((:channel __channel) (make-array 0 :initial-element 0 :element-type :integer))
    ((:state __state) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _channel __channel)
   (setq _state __state)
   self)
  (:channel
   (&optional __channel)
   (if __channel (setq _channel __channel)) _channel)
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:serialization-length
   ()
   (+
    ;; int8[] _channel
    (* 1    (length _channel)) 4
    ;; int8[] _state
    (* 1    (length _state)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8[] _channel
     (write-long (length _channel) s)
     (dotimes (i (length _channel))
       (write-byte (elt _channel i) s)
       )
     ;; int8[] _state
     (write-long (length _state) s)
     (dotimes (i (length _state))
       (write-byte (elt _state i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8[] _channel
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _channel (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _channel i) (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> (elt _channel i) 127) (setf (elt _channel i) (- (elt _channel i) 256)))
     ))
   ;; int8[] _state
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _state (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _state i) (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> (elt _state i) 127) (setf (elt _state i) (- (elt _state i) 256)))
     ))
   ;;
   self)
  )

(defclass papouch_ros::WriteIOResponse
  :super ros::object
  :slots (_retval ))

(defmethod papouch_ros::WriteIOResponse
  (:init
   (&key
    ((:retval __retval) nil)
    )
   (send-super :init)
   (setq _retval __retval)
   self)
  (:retval
   (&optional __retval)
   (if __retval (setq _retval __retval)) _retval)
  (:serialization-length
   ()
   (+
    ;; bool _retval
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _retval
       (if _retval (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _retval
     (setq _retval (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass papouch_ros::WriteIO
  :super ros::object
  :slots ())

(setf (get papouch_ros::WriteIO :md5sum-) "acedff32d14bc005248c00858b1d9393")
(setf (get papouch_ros::WriteIO :datatype-) "papouch_ros/WriteIO")
(setf (get papouch_ros::WriteIO :request) papouch_ros::WriteIORequest)
(setf (get papouch_ros::WriteIO :response) papouch_ros::WriteIOResponse)

(defmethod papouch_ros::WriteIORequest
  (:response () (instance papouch_ros::WriteIOResponse :init)))

(setf (get papouch_ros::WriteIORequest :md5sum-) "acedff32d14bc005248c00858b1d9393")
(setf (get papouch_ros::WriteIORequest :datatype-) "papouch_ros/WriteIORequest")
(setf (get papouch_ros::WriteIORequest :definition-)
      "
# List of IO channels to write.
int8[] channel

# List of state
int8[] state
---
bool retval

")

(setf (get papouch_ros::WriteIOResponse :md5sum-) "acedff32d14bc005248c00858b1d9393")
(setf (get papouch_ros::WriteIOResponse :datatype-) "papouch_ros/WriteIOResponse")
(setf (get papouch_ros::WriteIOResponse :definition-)
      "
# List of IO channels to write.
int8[] channel

# List of state
int8[] state
---
bool retval

")



(provide :papouch_ros/WriteIO "acedff32d14bc005248c00858b1d9393")


