CREATE TABLE driver(
	-- A00-00-000000
	license_no VARCHAR(15) CHECK (license_no LIKE '___-__-______') PRIMARY KEY,	

	last_name VARCHAR(50) NOT NULL,
	first_name VARCHAR(50) NOT NULL,
	middle_name VARCHAR(50) NOT NULL,
	suffix VARCHAR(50),

	-- YYYY-MM-DD
	dob DATE NOT NULL,
	
	-- derived age on View

	-- F/M
	sex VARCHAR(1) CHECK (sex IN ('M', 'F')) NOT NULL,

	-- NP/P/SP
	license_type VARCHAR(2) CHECK (license_type IN ('NP', 'P', 'SP')) NOT NULL,
	
	license_status VARCHAR(10) CHECK (license_status IN ('Valid', 'Expired', 'Suspended', 'Revoked')) NOT NULL ,
	license_issued DATE NOT NULL,
	license_expire DATE NOT NULL

	);

CREATE TABLE driver_address(
	d_address VARCHAR(50) PRIMARY KEY,
	d_street VARCHAR(50) NOT NULL,
	d_barangay VARCHAR(50) NOT NULL,
	d_city VARCHAR(50) NOT NULL,
	d_region VARCHAR(50) NOT NULL
	
	-- Di ko pa alam pano yung constraint sa postgresql
	-- CONSTRAINT driver_license_no_pk PRIMARY KEY(license_no)

	);

CREATE TABLE vehicle(
	-- Gagawan ko pa ng constraint
	plate_no VARCHAR(15) PRIMARY KEY,
	v_type VARCHAR(20) NOT NULL,
	v_make VARCHAR(20) NOT NULL,
	v_model VARCHAR(20) NOT NULL,
	v_color VARCHAR(20) NOT NULL,
	v_year INT(4) NOT NULL,
	engine_no VARCHAR(20) NOT NULL,
	chassis_no VARCHAR(20) NOT NULL,
	
	-- Di ko pa alam pano yung constraint sa postgresql
	-- CONSTRAINT driver_license_no_fk FOREIGN KEY(license_no)

	);

CREATE TABLE vehicle_reg(
	-- Not sure kung iba pa sa plate number
	reg_no VARCHAR(20) PRIMARY KEY,
	reg_status VARCHAR(20) NOT NULL,
	reg_date DATE NOT NULL,
	exp_date DATE NOT NULL,

	-- Di ko pa alam pano yung constraint sa postgresql
	-- CONSTRAINT vehicle_plate_no_fk FOREIGN KEY(plate_no)

	);

CREATE TABLE traffic_vio(
	tv_id VARCHAR(10) PRIMARY KEY,
	tv_type VARCHAR(20) NOT NULL,
	tv_status VARCHAR(20) NOT NULL,
	tv_date DATE NOT NULL,
	tv_street VARCHAR(50) NOT NULL,
	tv_barangay VARCHAR(50) NOT NULL,
	tv_city VARCHAR(50) NOT NULL,
	tv_region VARCHAR(50) NOT NULL,
	tv_fine INT(5) NOT NULL,
	app_officer VARCHAR(50),

	-- Di ko pa alam pano yung constraint sa postgresql
	-- CONSTRAINT driver_license_no_fk FOREIGN KEY(license_no)
	-- CONSTRAINT vehicle_plate_no_fk FOREIGN KEY(plate_no)

	);