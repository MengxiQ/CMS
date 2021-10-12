const connectorRules = [
  {
    type: 'Service',
    canBeContainedType: ['Service'],
    canLinkToType: ['Service']
  },
  {
    type: 'Root',
    canBeContainedType: ['Root', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager'],
    canLinkToType: ['Root', 'Compute', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager']
  },
  {
    type: 'Compute',
    canBeContainedType: [],
    canLinkToType: ['Compute', 'Root', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'Network', 'VirtualIP', 'SercurityGroup', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'ApplicationModule', 'CloudifyManager']
  },
  {
    type: 'Container',
    canBeContainedType: ['Container', 'Compute'],
    canLinkToType: ['Container', 'Root', 'Volume', 'FileSystem', 'ObjectStorage', 'Network', 'VirtualIP', 'SercurityGroup', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'ApplicationModule', 'CloudifyManager']
  },
  {
    type: 'Volume',
    canBeContainedType: ['Root', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager'],
    canLinkToType: ['Volume', 'Root', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager']
  },
  {
    type: 'FileSystem',
    canBeContainedType: ['FileSystem', 'Root', 'Compute', 'Container', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager'],
    canLinkToType: ['FileSystem', 'Root', 'Compute', 'Container', 'Volume', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'ApplicationModule', 'CloudifyManager']
  },
  {
    type: 'ObjectStorage',
    canBeContainedType: ['ObjectStorage', 'Root', 'Compute', 'Container', 'FileSystem', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager'],
    canLinkToType: ['ObjectStorage', 'Root', 'Compute', 'Container', 'Volume', 'FileSystem', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'ApplicationModule', 'CloudifyManager']
  },
  {
    type: 'Network',
    canBeContainedType: [],
    canLinkToType: []
  },
  {
    type: 'Router',
    canBeContainedType: [],
    canLinkToType: []
  },
  {
    type: 'LoadBalancer',
    canBeContainedType: [],
    canLinkToType: []
  },
  {
    type: 'VirtualIP',
    canBeContainedType: [],
    canLinkToType: []
  },
  {
    type: 'SercurityGroup',
    canBeContainedType: [],
    canLinkToType: []
  },
  {
    type: 'DBMS',
    canBeContainedType: ['DBMS', 'Root', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager'],
    canLinkToType: ['DBMS', 'Root', 'Compute', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager']
  },
  {
    type: 'DataBase',
    canBeContainedType: ['DataBase', 'Root', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DBMS', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager'],
    canLinkToType: ['DataBase', 'Root', 'Compute', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'DBMS', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'CloudifyManager']
  },
  {
    type: 'WebServer',
    canBeContainedType: ['WebServer', 'Root', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'ApplicationServer', 'CloudifyManager'],
    canLinkToType: ['WebServer', 'Root', 'Compute', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'ApplicationServer', 'CloudifyManager']
  },
  {
    type: 'ApplicationServer',
    canBeContainedType: ['ApplicationServer', 'Root', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'CloudifyManager'],
    canLinkToType: ['ApplicationServer', 'Root', 'Compute', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'CloudifyManager']
  },
  {
    type: 'MessageBusServer',
    canBeContainedType: ['ApplicationServer', 'Root', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'CloudifyManager'],
    canLinkToType: ['ApplicationServer', 'Root', 'Compute', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'CloudifyManager']
  },
  {
    type: 'switch',
    canBeContainedType: [],
    canLinkToType: ['switch', 'ApplicationModule', 'Root', 'Compute', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'CloudifyManager']
  },
  {
    type: 'CloudifyManager',
    canBeContainedType: ['CloudifyManager', 'Compute', 'Container', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer'],
    canLinkToType: ['CloudifyManager', 'Compute', 'Container', 'Volume', 'FileSystem', 'ObjectStorage', 'DBMS', 'DataBase', 'WebServer', 'ApplicationServer', 'MessageBusServer', 'ApplicationModule']
  }
]
export default connectorRules
