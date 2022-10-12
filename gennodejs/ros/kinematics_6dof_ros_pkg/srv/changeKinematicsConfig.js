// Auto-generated. Do not edit!

// (in-package kinematics_6dof_ros_pkg.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class changeKinematicsConfigRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.configuration = null;
      this.eef_robot_frame = null;
    }
    else {
      if (initObj.hasOwnProperty('configuration')) {
        this.configuration = initObj.configuration
      }
      else {
        this.configuration = '';
      }
      if (initObj.hasOwnProperty('eef_robot_frame')) {
        this.eef_robot_frame = initObj.eef_robot_frame
      }
      else {
        this.eef_robot_frame = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type changeKinematicsConfigRequest
    // Serialize message field [configuration]
    bufferOffset = _serializer.string(obj.configuration, buffer, bufferOffset);
    // Serialize message field [eef_robot_frame]
    bufferOffset = _serializer.string(obj.eef_robot_frame, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type changeKinematicsConfigRequest
    let len;
    let data = new changeKinematicsConfigRequest(null);
    // Deserialize message field [configuration]
    data.configuration = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [eef_robot_frame]
    data.eef_robot_frame = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.configuration.length;
    length += object.eef_robot_frame.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'kinematics_6dof_ros_pkg/changeKinematicsConfigRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7610575331dca08deb1829a93e58249c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string configuration
    string eef_robot_frame
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new changeKinematicsConfigRequest(null);
    if (msg.configuration !== undefined) {
      resolved.configuration = msg.configuration;
    }
    else {
      resolved.configuration = ''
    }

    if (msg.eef_robot_frame !== undefined) {
      resolved.eef_robot_frame = msg.eef_robot_frame;
    }
    else {
      resolved.eef_robot_frame = ''
    }

    return resolved;
    }
};

class changeKinematicsConfigResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.result = null;
    }
    else {
      if (initObj.hasOwnProperty('result')) {
        this.result = initObj.result
      }
      else {
        this.result = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type changeKinematicsConfigResponse
    // Serialize message field [result]
    bufferOffset = _serializer.string(obj.result, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type changeKinematicsConfigResponse
    let len;
    let data = new changeKinematicsConfigResponse(null);
    // Deserialize message field [result]
    data.result = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.result.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'kinematics_6dof_ros_pkg/changeKinematicsConfigResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c22f2a1ed8654a0b365f1bb3f7ff2c0f';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string result
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new changeKinematicsConfigResponse(null);
    if (msg.result !== undefined) {
      resolved.result = msg.result;
    }
    else {
      resolved.result = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: changeKinematicsConfigRequest,
  Response: changeKinematicsConfigResponse,
  md5sum() { return 'f5f869dd94ca439f0a9ec55af2a70f63'; },
  datatype() { return 'kinematics_6dof_ros_pkg/changeKinematicsConfig'; }
};
