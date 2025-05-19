// App.js
// Componente principal de la aplicación
// Maneja la navegación y la pantalla de login

import React, { useState, useEffect } from 'react';
import axios from 'axios';

// --- Iconos (ejemplos, puedes usar una librería como react-icons) ---
const UsersIcon = () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
  <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
</svg>;

const WifiIcon = () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
  <path strokeLinecap="round" strokeLinejoin="round" d="M8.288 15.038a5.25 5.25 0 017.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 011.06 0z" />
</svg>;

const SensorIcon = () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 4.5a.75.75 0 00-.75.75v13.5a.75.75 0 00.75.75h16.5a.75.75 0 00.75-.75V5.25a.75.75 0 00-.75-.75H3.75zM10.5 12a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5zM13.5 10.5a.75.75 0 000 1.5h3a.75.75 0 000-1.5h-3z" />
</svg>;

const CarIcon = () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v.958m12 0c.272 0 .53.05.77.141m-6.77 0a48.459 48.459 0 01-4.46 0m4.46 0S10.23 6.75 10.5 6.75M7.5 18.75c0-1.173.164-2.296.46-3.348M16.5 18.75c0-1.173-.164-2.296-.46-3.348" />
</svg>;

const DashboardIcon = () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h12A2.25 2.25 0 0020.25 14.25V3m-16.5 0h16.5M3.75 3c0-1.125.75-2.25 2.25-2.25h12c1.5 0 2.25 1.125 2.25 2.25M3.75 7.5h16.5M3.75 11.25h16.5M10.5 16.5c0 .621.504 1.125 1.125 1.125h.75c.621 0 1.125-.504 1.125-1.125v-2.25c0-.621-.504-1.125-1.125-1.125h-.75A1.125 1.125 0 0010.5 14.25v2.25z" />
</svg>;

const SettingsIcon = () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
 <path strokeLinecap="round" strokeLinejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.39.39 1.024 0 1.414l-.527.737c-.25.35-.272.806-.108 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.11v1.093c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.142.854.107 1.204l.527.738c.39.39.39 1.023 0 1.414l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.78.93l-.15.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527a1.125 1.125 0 01-1.45-.12l-.773-.774a1.125 1.125 0 010-1.414l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.506-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.11v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.142-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.93l.15-.893z" />
  <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
</svg>;

const LogoutIcon = () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
</svg>;


// --- Componentes Reutilizables ---
const PageTitle = ({ title }) => (
  <h2 className="text-xl font-semibold text-gray-500 mb-4 mt-6 first:mt-0 uppercase tracking-wider">{title}</h2>
);

const Card = ({ children, title, className="" }) => (
  <div className={`bg-white shadow-lg rounded-lg p-6 mb-6 ${className}`}>
    {title && <h3 className="text-2xl font-semibold text-gray-700 mb-6 text-center">{title}</h3>}
    {children}
  </div>
);

const Button = ({ children, onClick, type = "primary", className = "", fullWidth = false }) => {
  const baseStyle = "px-6 py-3 rounded-md font-semibold focus:outline-none focus:ring-2 focus:ring-opacity-75 transition-colors duration-150 ease-in-out";
  const typeStyles = {
    primary: "bg-red-600 hover:bg-red-700 text-white focus:ring-red-500", // Color principal como el de "Arsenal"
    secondary: "bg-gray-200 hover:bg-gray-300 text-gray-700 focus:ring-gray-400",
    danger: "bg-red-500 hover:bg-red-600 text-white focus:ring-red-400",
    link: "text-blue-600 hover:text-blue-800 hover:underline",
  };
  return (
    <button onClick={onClick} className={`${baseStyle} ${typeStyles[type]} ${fullWidth ? 'w-full' : ''} ${className}`}>
      {children}
    </button>
  );
};

const InputField = ({ label, type = "text", placeholder, value, onChange, id, name }) => (
  <div className="mb-6">
    <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
    <input
      type={type}
      id={id}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm"
    />
  </div>
);

const SelectField = ({ label, options, value, onChange, id }) => (
  <div className="mb-4">
    <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
    <select
      id={id}
      value={value}
      onChange={onChange}
      className="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
    >
      {options.map(option => (
        <option key={option.value} value={option.value}>{option.label}</option>
      ))}
    </select>
  </div>
);

// --- Pantalla de Login ---
const LoginScreen = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('/api/login/', { email, password });
      if (response.data.success) {
        onLoginSuccess();
      } else {
        setError("Correo electrónico o contraseña incorrectos.");
      }
    } catch (err) {
      setError("Correo electrónico o contraseña incorrectos.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center items-center p-4 font-inter">
      <div className="w-full max-w-md">
        <Card className="bg-white shadow-2xl rounded-xl p-8">
          <div className="text-center mb-8">
            {/* Placeholder para el logo de Arsenal */}
            <div className="bg-red-600 text-white w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-4xl font-bold">A</span> {/* Simulación de logo */}
            </div>
            <h2 className="text-3xl font-bold text-gray-800">Ingresar</h2>
            <p className="text-gray-500">Favor de ingresar usuario y contraseña para continuar</p>
          </div>

          <form onSubmit={handleSubmit}>
            <InputField
              id="email"
              name="email"
              label="Correo Electrónico"
              type="email"
              placeholder="tu@correo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <InputField
              id="password"
              name="password"
              label="Contraseña"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}
            <Button type="primary" fullWidth className="py-3 text-lg">
              Ingresar
            </Button>
          </form>
          <div className="mt-6 text-center">
            <Button type="link" onClick={() => alert("Funcionalidad 'Olvidé la contraseña' no implementada.")}>
              Olvidé la contraseña
            </Button>
          </div>
        </Card>
        <div className="text-center mt-8">
          <h1 className="text-4xl font-bold text-red-600">Arsenal</h1>
          <p className="text-gray-600">TPMS Solutions</p>
        </div>
      </div>
    </div>
  );
};


// --- Componentes de Vista (Placeholder) ---
// (ClientRegistry, UserInvitation, etc. permanecen igual, se omiten aquí por brevedad)
// 1. Registro de Clientes
const ClientRegistry = () => {
  const [clientName, setClientName] = useState('');
  const [clientContact, setClientContact] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Registrando cliente:", { clientName, clientContact });
    alert("Cliente registrado (simulación)");
  };

  return (
    <Card title="Registro de Nuevo Cliente">
      <form onSubmit={handleSubmit}>
        <InputField
          id="clientName"
          label="Nombre del Cliente"
          placeholder="Ej: Transporte Veloz S.A."
          value={clientName}
          onChange={(e) => setClientName(e.target.value)}
        />
        <InputField
          id="clientContact"
          label="Información de Contacto"
          placeholder="Ej: contacto@transporteveloz.com / +58 212 555 1234"
          value={clientContact}
          onChange={(e) => setClientContact(e.target.value)}
        />
        <Button type="primary">Registrar Cliente</Button>
      </form>
    </Card>
  );
};

// 2. Usuarios por Clientes (Códigos de Invitación)
const UserInvitation = () => {
  const [selectedClient, setSelectedClient] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [invitationCode, setInvitationCode] = useState('');

  const clients = [
    { value: 'client1', label: 'Transporte Veloz S.A.' },
    { value: 'client2', label: 'Logística Rápida C.A.' },
  ];

  const handleGenerateCode = () => {
    const code = Math.random().toString(36).substring(2, 10).toUpperCase();
    setInvitationCode(code);
    console.log("Código de invitación generado:", code, "para", userEmail, "del cliente", selectedClient);
  };

  return (
    <Card title="Gestión de Usuarios por Cliente">
      <SelectField
        id="selectClientUser"
        label="Seleccionar Cliente"
        options={[{ value: '', label: 'Seleccione un cliente' }, ...clients]}
        value={selectedClient}
        onChange={(e) => setSelectedClient(e.target.value)}
      />
      <InputField
        id="userEmail"
        label="Email del Usuario a Invitar"
        type="email"
        placeholder="usuario@ejemplo.com"
        value={userEmail}
        onChange={(e) => setUserEmail(e.target.value)}
      />
      <Button onClick={handleGenerateCode} className="mr-2">Generar Código de Invitación</Button>
      {invitationCode && (
        <div className="mt-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded-md">
          <p className="font-semibold">Código Generado: {invitationCode}</p>
        </div>
      )}
    </Card>
  );
};

// 3. Registro de Receptores a Clientes
const ReceiverRegistry = () => {
  const [selectedClientReceiver, setSelectedClientReceiver] = useState('');
  const [receiverId, setReceiverId] = useState('');
  const [receiverLocation, setReceiverLocation] = useState('');

  const clients = [
    { value: 'client1', label: 'Transporte Veloz S.A.' },
    { value: 'client2', label: 'Logística Rápida C.A.' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Registrando receptor:", { selectedClientReceiver, receiverId, receiverLocation });
    alert("Receptor registrado (simulación)");
  };

  return (
    <Card title="Registro de Receptores">
      <form onSubmit={handleSubmit}>
        <SelectField
          id="selectClientReceiver"
          label="Asignar a Cliente"
          options={[{ value: '', label: 'Seleccione un cliente' }, ...clients]}
          value={selectedClientReceiver}
          onChange={(e) => setSelectedClientReceiver(e.target.value)}
        />
        <InputField
          id="receiverId"
          label="ID del Receptor"
          placeholder="Ej: RECEPTOR-001"
          value={receiverId}
          onChange={(e) => setReceiverId(e.target.value)}
        />
        <InputField
          id="receiverLocation"
          label="Ubicación del Receptor (Opcional)"
          placeholder="Ej: Oficina Principal, Taller"
          value={receiverLocation}
          onChange={(e) => setReceiverLocation(e.target.value)}
        />
        <Button type="primary">Registrar Receptor</Button>
      </form>
    </Card>
  );
};

// 4. Registro de Sensores a Receptores
const SensorRegistry = () => {
  const [selectedReceiver, setSelectedReceiver] = useState('');
  const [sensorId, setSensorId] = useState('');
  const [sensorType, setSensorType] = useState('presion_temperatura');

  const receivers = [
    { value: 'receptor1', label: 'RECEPTOR-001 (Transporte Veloz)' },
    { value: 'receptor2', label: 'RECEPTOR-002 (Logística Rápida)' },
  ];

  const sensorTypes = [
    { value: 'presion_temperatura', label: 'Presión y Temperatura' },
    { value: 'presion', label: 'Solo Presión' },
    { value: 'temperatura', label: 'Solo Temperatura' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Registrando sensor:", { selectedReceiver, sensorId, sensorType });
    alert("Sensor registrado (simulación)");
  };
  return (
    <Card title="Registro de Sensores">
      <form onSubmit={handleSubmit}>
        <SelectField
          id="selectReceiverSensor"
          label="Asignar a Receptor"
          options={[{ value: '', label: 'Seleccione un receptor' }, ...receivers]}
          value={selectedReceiver}
          onChange={(e) => setSelectedReceiver(e.target.value)}
        />
        <InputField
          id="sensorId"
          label="ID del Sensor"
          placeholder="Ej: SENSOR-TPMS-XYZ123"
          value={sensorId}
          onChange={(e) => setSensorId(e.target.value)}
        />
        <SelectField
          id="sensorType"
          label="Tipo de Sensor"
          options={sensorTypes}
          value={sensorType}
          onChange={(e) => setSensorType(e.target.value)}
        />
        <Button type="primary">Registrar Sensor</Button>
      </form>
    </Card>
  );
};

// 5. Registro de Vehículos de Clientes
const VehicleRegistry = () => {
  const [selectedClientVehicle, setSelectedClientVehicle] = useState('');
  const [vehiclePlate, setVehiclePlate] = useState('');
  const [vehicleModel, setVehicleModel] = useState('');
  const [vehicleType, setVehicleType] = useState('camion_gandola');

  const clients = [
    { value: 'client1', label: 'Transporte Veloz S.A.' },
    { value: 'client2', label: 'Logística Rápida C.A.' },
  ];

  const vehicleTypes = [
    { value: 'camion_gandola', label: 'Camión Gandola (Chuto + Batea)' },
    { value: 'camion_750', label: 'Camión 750' },
    { value: 'autobus', label: 'Autobús' },
    { value: 'pickup', label: 'Pickup' },
    { value: 'otro', label: 'Otro' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Registrando vehículo:", { selectedClientVehicle, vehiclePlate, vehicleModel, vehicleType });
    alert("Vehículo registrado (simulación)");
  };

  return (
    <Card title="Registro de Vehículos">
      <form onSubmit={handleSubmit}>
        <SelectField
          id="selectClientVehicle"
          label="Propietario (Cliente)"
          options={[{ value: '', label: 'Seleccione un cliente' }, ...clients]}
          value={selectedClientVehicle}
          onChange={(e) => setSelectedClientVehicle(e.target.value)}
        />
        <InputField
          id="vehiclePlate"
          label="Placa del Vehículo"
          placeholder="Ej: A01BC2D"
          value={vehiclePlate}
          onChange={(e) => setVehiclePlate(e.target.value)}
        />
        <InputField
          id="vehicleModel"
          label="Modelo/Marca del Vehículo"
          placeholder="Ej: Mack Anthem / Ford Cargo 1721"
          value={vehicleModel}
          onChange={(e) => setVehicleModel(e.target.value)}
        />
        <SelectField
          id="vehicleType"
          label="Tipo de Vehículo"
          options={vehicleTypes}
          value={vehicleType}
          onChange={(e) => setVehicleType(e.target.value)}
        />
        <Button type="primary">Registrar Vehículo</Button>
      </form>
    </Card>
  );
};

// 6. Asignación de Sensores a Posiciones del Vehículo
const SensorAssignment = () => {
  const [selectedVehicle, setSelectedVehicle] = useState('');
  const [selectedSensor, setSelectedSensor] = useState('');
  const [tirePosition, setTirePosition] = useState('');

  const vehicles = [
    { value: 'vehicle1', label: 'A01BC2D (Mack Anthem)' },
    { value: 'vehicle2', label: 'X45YZ6F (Ford Cargo)' },
  ];
  const sensors = [
    { value: 'sensor1', label: 'SENSOR-TPMS-XYZ123' },
    { value: 'sensor2', label: 'SENSOR-TPMS-ABC789' },
    { value: 'sensor3', label: 'SENSOR-TPMS-DEF456' },
  ];
  const positions = [
    { value: 'del_izq_ext', label: 'Delantera Izquierda Externa' },
    { value: 'del_izq_int', label: 'Delantera Izquierda Interna' },
    // ... más posiciones
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Asignando sensor:", { selectedVehicle, selectedSensor, tirePosition });
    alert("Sensor asignado a posición (simulación)");
  };

  return (
    <Card title="Asignación de Sensores a Vehículo">
      <form onSubmit={handleSubmit}>
        <SelectField
          id="selectVehicleForSensor"
          label="Seleccionar Vehículo"
          options={[{ value: '', label: 'Seleccione un vehículo' }, ...vehicles]}
          value={selectedVehicle}
          onChange={(e) => setSelectedVehicle(e.target.value)}
        />
        <SelectField
          id="selectSensorForAssignment"
          label="Seleccionar Sensor (Disponible)"
          options={[{ value: '', label: 'Seleccione un sensor' }, ...sensors]}
          value={selectedSensor}
          onChange={(e) => setSelectedSensor(e.target.value)}
        />
        <SelectField
          id="selectTirePosition"
          label="Posición en el Vehículo"
          options={[{ value: '', label: 'Seleccione una posición' }, ...positions]}
          value={tirePosition}
          onChange={(e) => setTirePosition(e.target.value)}
        />
        <Button type="primary">Asignar Sensor</Button>
      </form>
    </Card>
  );
};

// --- Componente de Esquema de Vehículo ---
const VehicleSchematic = ({ vehicleType = "camion_gandola", sensorData }) => {
  const renderTire = (label, positionKey) => {
    const data = sensorData && sensorData[positionKey];
    const pressure = data ? data.pressure : "N/A";
    const temp = data ? data.temp : "N/A";
    let borderColor = 'border-gray-300'; // Default
    if (data) {
        if (data.pressure < 30 || data.pressure > 110) borderColor = 'border-red-500 animate-pulse'; // Alerta presión
        else if (data.temp > 60) borderColor = 'border-orange-500'; // Advertencia temperatura
        else borderColor = 'border-green-500'; // OK
    }


    return (
      <div className={`border-2 rounded-md p-2 m-1 text-center shadow-sm ${borderColor} transition-all duration-300`}>
        <div className="font-semibold text-sm text-gray-700">{label}</div>
        <div className="text-xs text-gray-600">P: {pressure} PSI</div>
        <div className="text-xs text-gray-600">T: {temp}°C</div>
      </div>
    );
  };

  if (vehicleType === "camion_gandola") {
    return (
      <div className="bg-gray-50 p-4 rounded-lg shadow">
        <h4 className="font-semibold mb-3 text-center text-gray-700">Esquema del Vehículo (Gandola)</h4>
        {/* Chuto */}
        <div className="mb-4">
          <p className="text-sm text-center font-medium text-gray-500 mb-2">CHUTO</p>
          <div className="grid grid-cols-2 gap-1 mb-2">
            {renderTire("DI Ext", "chuto_del_izq_ext")}
            {renderTire("DD Ext", "chuto_del_der_ext")}
            {renderTire("DI Int", "chuto_del_izq_int")}
            {renderTire("DD Int", "chuto_del_der_int")}
          </div>
          <div className="grid grid-cols-2 gap-1">
            {renderTire("TRI Ext", "chuto_tra_izq_ext")}
            {renderTire("TRD Ext", "chuto_tra_der_ext")}
            {renderTire("TRI Int", "chuto_tra_izq_int")}
            {renderTire("TRD Int", "chuto_tra_der_int")}
          </div>
        </div>
        {/* Batea */}
        <div>
          <p className="text-sm text-center font-medium text-gray-500 mb-2">BATEA</p>
          {[1, 2, 3].map(eje => ( // Asumiendo hasta 3 ejes en batea
            <div key={`batea_eje_${eje}`} className="grid grid-cols-2 gap-1 mb-2">
              {renderTire(`BI${eje} Ext`, `batea_e${eje}_izq_ext`)}
              {renderTire(`BD${eje} Ext`, `batea_e${eje}_der_ext`)}
              {renderTire(`BI${eje} Int`, `batea_e${eje}_izq_int`)}
              {renderTire(`BD${eje} Int`, `batea_e${eje}_der_int`)}
            </div>
          ))}
        </div>
      </div>
    );
  }
  // Podrías añadir más 'else if' para otros tipos de vehículos
  return <p className="text-gray-500 p-4 text-center">Seleccione un tipo de vehículo compatible para ver el esquema.</p>;
};


// 7. Monitoreo (Temperatura, Presión, Localización)
const MonitoringDashboard = () => {
  const [selectedVehicleMonitor, setSelectedVehicleMonitor] = useState('');
  const [sensorData, setSensorData] = useState({}); // Inicialmente vacío

  const vehicles = [
    { value: 'vehicle1', label: 'A01BC2D (Mack Anthem - Gandola)' , type: 'camion_gandola' },
    { value: 'vehicle2', label: 'X45YZ6F (Ford Cargo - Camión 750)', type: 'camion_750' }, // Necesitarías un esquema para este
  ];
  
  const currentVehicle = vehicles.find(v => v.value === selectedVehicleMonitor);

  // Simulación: Cargar y actualizar datos
  useEffect(() => {
    if (!selectedVehicleMonitor) {
      setSensorData({}); // Limpiar datos si no hay vehículo seleccionado
      return;
    }

    // Carga inicial de datos para el vehículo seleccionado
    const initialData = { // Datos de ejemplo para gandola
      'chuto_del_izq_ext': { pressure: 100, temp: 28 }, 'chuto_del_der_ext': { pressure: 102, temp: 29 },
      'chuto_del_izq_int': { pressure: 101, temp: 27 }, 'chuto_del_der_int': { pressure: 99, temp: 30 },
      'chuto_tra_izq_ext': { pressure: 105, temp: 35 }, 'chuto_tra_der_ext': { pressure: 103, temp: 36 },
      'chuto_tra_izq_int': { pressure: 104, temp: 34 }, 'chuto_tra_der_int': { pressure: 106, temp: 35 },
      'batea_e1_izq_ext': { pressure: 100, temp: 33 }, 'batea_e1_der_ext': { pressure: 102, temp: 32 },
      'batea_e1_izq_int': { pressure: 101, temp: 31 }, 'batea_e1_der_int': { pressure: 99, temp: 33 },
      'batea_e2_izq_ext': { pressure: 103, temp: 34 }, 'batea_e2_der_ext': { pressure: 100, temp: 35 },
      'batea_e2_izq_int': { pressure: 102, temp: 32 }, 'batea_e2_der_int': { pressure: 104, temp: 34 },
      'batea_e3_izq_ext': { pressure: 98, temp: 35 }, 'batea_e3_der_ext': { pressure: 101, temp: 36 }, // Eje 3
      'batea_e3_izq_int': { pressure: 100, temp: 33 }, 'batea_e3_der_int': { pressure: 102, temp: 35 },
    };
    setSensorData(initialData);

    const intervalId = setInterval(() => {
      console.log("Actualizando datos de monitoreo para:", selectedVehicleMonitor);
      setSensorData(prevData => {
        const newData = { ...prevData };
        for (const key in newData) {
          if (newData[key]) { // Verificar que la propiedad exista
            newData[key].pressure = Math.max(25, Math.min(125, newData[key].pressure + (Math.random() * 4 - 2))); // fluctuación +/- 2 PSI
            newData[key].temp = Math.max(15, Math.min(85, newData[key].temp + (Math.random() * 2 - 1)));    // fluctuación +/- 1 C
          }
        }
        return newData;
      });
    }, 5000); 

    return () => clearInterval(intervalId);
  }, [selectedVehicleMonitor]);


  return (
    <Card title="Panel de Monitoreo en Tiempo Real" className="!p-0 md:!p-6">
      <div className="p-4 md:p-0">
        <SelectField
            id="selectVehicleMonitor"
            label="Seleccionar Vehículo a Monitorear"
            options={[{ value: '', label: 'Seleccione un vehículo' }, ...vehicles]}
            value={selectedVehicleMonitor}
            onChange={(e) => setSelectedVehicleMonitor(e.target.value)}
        />
      </div>

      {selectedVehicleMonitor && currentVehicle ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-2">
          <div className="lg:col-span-2">
            <VehicleSchematic vehicleType={currentVehicle.type} sensorData={sensorData} />
          </div>
          <div className="lg:col-span-1">
            <Card title="Detalles Adicionales" className="!shadow-none md:!shadow-lg">
              <p className="text-sm text-gray-600 mb-2">
                <span className="font-semibold">Vehículo:</span> {currentVehicle.label}
              </p>
              <div className="mb-4">
                <h5 className="font-semibold text-gray-700 mb-1 text-sm">Alertas:</h5>
                {Object.values(sensorData).some(data => data && (data.pressure < 30 || data.pressure > 110 || data.temp > 70)) ? (
                    <div className="p-2 bg-red-100 border border-red-400 text-red-700 rounded-md text-sm">
                        <span className="font-semibold">¡Alerta!</span> Revise presiones/temperaturas.
                    </div>
                ) : (
                    <div className="p-2 bg-green-100 border border-green-400 text-green-700 rounded-md text-sm">
                        Sistema estable. Sin alertas.
                    </div>
                )}
              </div>
              
              <div>
                <h5 className="font-semibold text-gray-700 mb-1 text-sm">Localización (GPS):</h5>
                <p className="text-xs text-gray-500 italic mb-1">
                  Minutero de localización (funcionalidad futura).
                </p>
                <div className="w-full h-32 md:h-40 bg-gray-200 rounded-md flex items-center justify-center mt-1">
                  <p className="text-gray-400 text-sm">Mapa (GPS)</p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      ) : (
        <p className="text-center text-gray-500 mt-6 py-8">Por favor, seleccione un vehículo para ver los datos de monitoreo.</p>
      )}
    </Card>
  );
};


// --- Componente App Principal ---
function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Nuevo estado para el login

  // Nuevo estado para los datos, carga y error
  const [misDatos, setMisDatos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // --- INICIO: Estado y lógica para proyectos (portafolio) ---
  // const [projects, setProjects] = useState([]);
  // const [projectsLoading, setProjectsLoading] = useState(true);
  // const [projectsError, setProjectsError] = useState(null);

  // useEffect(() => {
  //   const fetchProjects = async () => {
  //     try {
  //       const response = await axios.get('http://localhost:8000/api/projects/');
  //       setProjects(response.data);
  //       setProjectsLoading(false);
  //     } catch (err) {
  //       setProjectsError(err.message || 'Ocurrió un error al obtener los proyectos.');
  //       setProjectsLoading(false);
  //     }
  //   };
  //   fetchProjects();
  // }, []);
  // --- FIN: Estado y lógica para proyectos (portafolio) ---

  // Simular verificación de sesión al cargar
  useEffect(() => {
    const loggedInStatus = localStorage.getItem('isLoggedInTPMS');
    if (loggedInStatus === 'true') {
      setIsLoggedIn(true);
    }
  }, []);

  // Consumir la API al montar el componente
  useEffect(() => {
    setLoading(true);
    setError('');
    axios.get('/api/misdatos/')
      .then(response => {
        setMisDatos(response.data);
        setLoading(false);
      })
      .catch(err => {
        setError('Error al cargar los datos');
        setLoading(false);
      });
  }, []);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    localStorage.setItem('isLoggedInTPMS', 'true'); // Guardar estado en localStorage
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentView('dashboard'); // Volver al dashboard por defecto al desloguear
    localStorage.removeItem('isLoggedInTPMS'); // Limpiar estado de localStorage
  };

  const renderView = () => {
    switch (currentView) {
      case 'clients': return <ClientRegistry />;
      case 'users': return <UserInvitation />;
      case 'receivers': return <ReceiverRegistry />;
      case 'sensors': return <SensorRegistry />;
      case 'vehicles': return <VehicleRegistry />;
      case 'assignment': return <SensorAssignment />;
      case 'dashboard':
      default: return <MonitoringDashboard />;
    }
  };

  const NavLink = ({ viewName, children, icon }) => (
    <button
      onClick={() => setCurrentView(viewName)}
      className={`flex items-center w-full px-4 py-3 text-left text-sm font-medium rounded-md transition-colors duration-150
                  ${currentView === viewName ? 'bg-red-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'}`}
    >
      {icon}
      {children}
    </button>
  );

  // Si no está logueado, mostrar la pantalla de Login
  if (!isLoggedIn) {
    return <LoginScreen onLoginSuccess={handleLoginSuccess} />;
  }

  // Si está logueado, mostrar la aplicación principal
  return (
    <div className="min-h-screen bg-gray-100 font-inter flex">
      <aside className="w-64 bg-white shadow-xl p-4 space-y-1 flex flex-col">
        <div className="text-center my-4">
             <div className="bg-red-600 text-white w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-2">
              <span className="text-2xl font-bold">A</span> {/* Simulación de logo */}
            </div>
            <div className="text-2xl font-bold text-red-700">Arsenal TPMS</div>
        </div>
        <nav className="flex-grow space-y-1">
          <NavLink viewName="dashboard" icon={<DashboardIcon />}>Monitoreo</NavLink>
          
          <PageTitle title="Registros"/>
          <NavLink viewName="clients" icon={<UsersIcon />}>Clientes</NavLink>
          <NavLink viewName="users" icon={<UsersIcon />}>Usuarios</NavLink>
          <NavLink viewName="receivers" icon={<WifiIcon />}>Receptores</NavLink>
          <NavLink viewName="sensors" icon={<SensorIcon />}>Sensores</NavLink>
          <NavLink viewName="vehicles" icon={<CarIcon />}>Vehículos</NavLink>
          
          <PageTitle title="Configuración"/>
          <NavLink viewName="assignment" icon={<SettingsIcon />}>Asignar Sensores</NavLink>
        </nav>
        <div className="mt-auto pt-2 border-t border-gray-200">
            <button
                onClick={handleLogout}
                className="flex items-center w-full px-4 py-3 text-left text-sm font-medium rounded-md text-gray-600 hover:bg-red-100 hover:text-red-700 transition-colors duration-150"
            >
                <LogoutIcon />
                Cerrar Sesión
            </button>
        </div>
      </aside>

      <main className="flex-1 p-6 md:p-8 overflow-y-auto">
        {renderView()}

        {/* --- INICIO: Sección de Portafolio de Proyectos --- */}
        {/*
        <section className="mt-12">
          <header className="mb-4">
            <h1 className="text-2xl font-bold text-gray-800">Portafolio de Proyectos</h1>
          </header>
          {projectsLoading ? (
            <div className="text-gray-500">Cargando proyectos...</div>
          ) : projectsError ? (
            <div className="text-red-500">Error al cargar los proyectos: {projectsError}</div>
          ) : (
            <div>
              {projects.length > 0 ? (
                <ul className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {projects.map(project => (
                    <li key={project.id} className="bg-white rounded-lg shadow p-4">
                      <h2 className="text-lg font-semibold">{project.title}</h2>
                      <p className="text-gray-600">{project.description}</p>
                      <p className="text-sm text-gray-500"><strong>Tecnología:</strong> {project.technology}</p>
                      <p className="text-xs text-gray-400 mt-1">
                        Creado el: {new Date(project.created_at).toLocaleDateString()}
                      </p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No hay proyectos disponibles en este momento.</p>
              )}
            </div>
          )}
        </section>
        */}
        {/* --- FIN: Sección de Portafolio de Proyectos --- */}
      </main>
      {/* ...existing code for API data list... */}
    </div>
  );
}

export default App;
