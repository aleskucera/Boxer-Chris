// Auto-generated. Do not edit!

// (in-package papouch_ros.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class WriteIORequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.channel = null;
      this.state = null;
    }
    else {
      if (initObj.hasOwnProperty('channel')) {
        this.channel = initObj.channel
      }
      else {
        this.channel = [];
      }
      if (initObj.hasOwnProperty('state')) {
        this.state = initObj.state
      }
      else {
        this.state = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type WriteIORequest
    // Serialize message field [channel]
    bufferOffset = _arraySerializer.int8(obj.channel, buffer, bufferOffset, null);
    // Serialize message field [state]
    bufferOffset = _arraySerializer.int8(obj.state, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type WriteIORequest
    let len;
    let data = new WriteIORequest(null);
    // Deserialize message field [channel]
    data.channel = _arrayDeserializer.int8(buffer, bufferOffset, null)
    // Deserialize message field [state]
    data.state = _arrayDeserializer.int8(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.channel.length;
    length += object.state.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'papouch_ros/WriteIORequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f441b6fe8c47b0a1a0e45816683dfd61';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    # List of IO channels to write.
    int8[] channel
    
    # List of state
    int8[] state
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new WriteIORequest(null);
    if (msg.channel !== undefined) {
      resolved.channel = msg.channel;
    }
    else {
      resolved.channel = []
    }

    if (msg.state !== undefined) {
      resolved.state = msg.state;
    }
    else {
      resolved.state = []
    }

    return resolved;
    }
};

class WriteIOResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.retval = null;
    }
    else {
      if (initObj.hasOwnProperty('retval')) {
        this.retval = initObj.retval
      }
      else {
        this.retval = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type WriteIOResponse
    // Serialize message field [retval]
    bufferOffset = _serializer.bool(obj.retval, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type WriteIOResponse
    let len;
    let data = new WriteIOResponse(null);
    // Deserialize message field [retval]
    data.retval = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'papouch_ros/WriteIOResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e60db45b9ec4a458523094ea4ee7553a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool retval
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new WriteIOResponse(null);
    if (msg.retval !== undefined) {
      resolved.retval = msg.retval;
    }
    else {
      resolved.retval = false
    }

    return resolved;
    }
};

module.exports = {
  Request: WriteIORequest,
  Response: WriteIOResponse,
  md5sum() { return 'acedff32d14bc005248c00858b1d9393'; },
  datatype() { return 'papouch_ros/WriteIO'; }
};
