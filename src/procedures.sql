set
  global transaction isolation level serializable;

set
  global SQL_MODE = 'ANSI,TRADITIONAL';

set
  names utf8mb4;

set
  SQL_SAFE_UPDATES = 0;

use restaurant_supply_express;

drop procedure if exists add_owner;

delimiter / / create procedure add_owner (
  in ip_username varchar(40),
  in ip_first_name varchar(100),
  in ip_last_name varchar(100),
  in ip_address varchar(500),
  in ip_birthdate date
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_username in (
    select
      username
    from
      users
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Username Already Exists!';

end if;

insert into
  users
values
  (
    ip_username,
    ip_first_name,
    ip_last_name,
    ip_address,
    ip_birthdate
  );

insert into
  restaurant_owners
values
  (ip_username);

end / / delimiter;

drop procedure if exists add_employee;

delimiter / / create procedure add_employee (
  in ip_username varchar(40),
  in ip_first_name varchar(100),
  in ip_last_name varchar(100),
  in ip_address varchar(500),
  in ip_birthdate date,
  in ip_taxID varchar(40),
  in ip_hired date,
  in ip_employee_experience integer,
  in ip_salary integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_username in (
    select
      username
    from
      employees
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Username Already Exists!';

end if;

if (
  ip_taxID in (
    select
      taxID
    from
      employees
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'TaxID Already Exists!';

end if;

insert into
  users value (
    ip_username,
    ip_first_name,
    ip_last_name,
    ip_address,
    ip_birthdate
  );

insert into
  employees
values
  (
    ip_username,
    ip_taxID,
    ip_hired,
    ip_employee_experience,
    ip_salary
  );

end / / delimiter;

drop procedure if exists add_pilot_role;

delimiter / / create procedure add_pilot_role (
  in ip_username varchar(40),
  in ip_licenseID varchar(40),
  in ip_pilot_experience integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_username not in (
    select
      username
    from
      employees
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Not An Employee!';

end if;

if (
  ip_username in (
    select
      username
    from
      pilots
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Already a Pilot!';

end if;

if (
  ip_licenseID in (
    select
      licenseID
    from
      pilots
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Duplicate License!';

end if;

insert into
  pilots
values
  (ip_username, ip_licenseID, ip_pilot_experience);

end / / delimiter;

drop procedure if exists add_worker_role;

delimiter / / create procedure add_worker_role (in ip_username varchar(40)) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_username not in (
    select
      username
    from
      employees
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Not An Employee!';

end if;

if (
  ip_username in (
    select
      username
    from
      workers
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Already a Woker!';

end if;

insert into
  workers
values
  (ip_username);

end / / delimiter;

drop procedure if exists add_ingredient;

delimiter / / create procedure add_ingredient (
  in ip_barcode varchar(40),
  in ip_iname varchar(100),
  in ip_weight integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_barcode in (
    select
      barcode
    from
      ingredients
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Duplicate Barcode!';

end if;

insert into
  ingredients
values
  (ip_barcode, ip_iname, ip_weight);

end / / delimiter;

drop procedure if exists add_drone;

delimiter / / create procedure add_drone (
  in ip_id varchar(40),
  in ip_tag integer,
  in ip_fuel integer,
  in ip_capacity integer,
  in ip_sales integer,
  in ip_flown_by varchar(40)
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  (ip_id, ip_tag) in (
    select
      id,
      tag
    from
      drones
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Duplicate Drone!';

end if;

if (
  ip_id not in (
    select
      id
    from
      delivery_services
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Delivery Service!';

end if;

if (
  ip_flown_by not in (
    select
      username
    from
      pilots natural
      join work_for
    where
      work_for.id = ip_id
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Pilot Not In Delivery Service!';

end if;

insert into
  drones
values
  (
    ip_id,
    ip_tag,
    ip_fuel,
    ip_capacity,
    ip_sales,
    ip_flown_by,
    NULL,
    NULL,
    (
      select
        home_base
      from
        delivery_services
      where
        ip_id = delivery_services.id
    )
  );

end / / delimiter;

drop procedure if exists add_restaurant;

delimiter / / create procedure add_restaurant (
  in ip_long_name varchar(40),
  in ip_rating integer,
  in ip_spent integer,
  in ip_location varchar(40)
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_long_name in (
    select
      long_name
    from
      restaurants
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Already Exists!';

end if;

if (
  ip_location not in (
    select
      label
    from
      locations
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Location!';

end if;

if (
  ip_rating > 5
  or ip_rating < 1
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Rating!';

end if;

insert into
  restaurants
values
  (
    ip_long_name,
    ip_rating,
    ip_spent,
    ip_location,
    NULL
  );

end / / delimiter;

drop procedure if exists add_service;

delimiter / / create procedure add_service (
  in ip_id varchar(40),
  in ip_long_name varchar(100),
  in ip_home_base varchar(40),
  in ip_manager varchar(40)
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_id in (
    select
      id
    from
      delivery_services
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Already Exists!';

end if;

if (
  ip_home_base not in (
    select
      label
    from
      locations
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Homebase!';

end if;

if (
  ip_manager not in (
    select
      username
    from
      workers
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Manager!';

end if;

insert into
  delivery_services
values
  (ip_id, ip_long_name, ip_home_base, ip_manager);

end / / delimiter;

drop procedure if exists add_location;

delimiter / / create procedure add_location (
  in ip_label varchar(40),
  in ip_x_coord integer,
  in ip_y_coord integer,
  in ip_space integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if(
  ip_label in (
    select
      label
    from
      locations
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Already Exists!';

end if;

if(
  (ip_x_coord, ip_y_coord) in (
    select
      x_coord,
      y_coord
    from
      locations
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Coordinates Already Exist!';

end if;

insert into
  locations
values
  (ip_label, ip_x_coord, ip_y_coord, ip_space);

end / / delimiter;

drop procedure if exists start_funding;

delimiter / / create procedure start_funding (
  in ip_owner varchar(40),
  in ip_long_name varchar(40)
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if(
  ip_owner not in (
    select
      username
    from
      restaurant_owners
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Onwer!';

end if;

if (
  ip_long_name not in (
    select
      long_name
    from
      restaurants
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Restaurant';

end if;

update
  restaurants
set
  funded_by = ip_owner
where
  long_name = ip_long_name;

end / / delimiter;

drop procedure if exists hire_employee;

delimiter / / create procedure hire_employee (in ip_username varchar(40), in ip_id varchar(40)) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  (ip_username, ip_id) in (
    select
      username,
      id
    from
      work_for
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Already Hired!';

end if;

if (
  ip_username not in (
    select
      username
    from
      employees
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Employee!';

end if;

if (
  ip_id not in (
    select
      id
    from
      delivery_services
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Delivery Service!';

end if;

if (
  ip_username in (
    select
      manager
    from
      delivery_services
    where
      id <> ip_id
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Manager Cannot Be Hired!';

end if;

if (
  ip_username in (
    select
      flown_by
    from
      drones natural
      join work_for
    where
      id <> ip_id
      and flown_by is not null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Pilot Already Controls Drones!';

end if;

insert into
  work_for
values
  (ip_username, ip_id);

end / / delimiter;

drop procedure if exists fire_employee;

delimiter / / create procedure fire_employee (in ip_username varchar(40), in ip_id varchar(40)) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_username not in (
    select
      username
    from
      work_for
    where
      ip_id = id
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Employee!';

end if;

if (
  ip_username in (
    select
      manager
    from
      delivery_services
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Cannot Fire Active Manager!';

end if;

if (
  ip_username in (
    select
      flown_by
    from
      drones
    where
      flown_by is not null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Cannot Fire Pilot Controlling Drones!';

end if;

delete from
  work_for
where
  (username, id) = (ip_username, ip_id);

end / / delimiter;

drop procedure if exists manage_service;

delimiter / / create procedure manage_service (in ip_username varchar(40), in ip_id varchar(40)) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  (ip_username, ip_id) not in (
    select
      username,
      id
    from
      work_for
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Employee';

end if;

if (
  ip_username in (
    select
      flown_by
    from
      drones
    where
      flown_by is not null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Pilot Controlling Drones Cannot Be Manager!';

end if;

if (
  ip_username in (
    select
      username
    from
      work_for
    where
      id <> ip_id
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Employee Already Hired By Another Service!';

end if;

if (
  ip_username not in (
    select
      username
    from
      workers
  )
) then
insert into
  workers
values
  (ip_username);

end if;

update
  delivery_services
set
  manager = ip_username
where
  id = ip_id;

end / / delimiter;

drop procedure if exists takeover_drone;

delimiter / / create procedure takeover_drone (
  in ip_username varchar(40),
  in ip_id varchar(40),
  in ip_tag integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_username not in (
    select
      username
    from
      work_for
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Pilot Not Working For This Service!';

end if;

if (
  (ip_id, ip_tag) not in (
    select
      drones.id,
      drones.tag
    from
      delivery_services natural
      join drones
    where
      delivery_services.id in (
        select
          id
        from
          work_for
        where
          ip_username = username
      )
  )
  or (ip_id, ip_tag) in (
    select
      id,
      tag
    from
      drones
    where
      flown_by is null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Drone!';

end if;

if (
  ip_username in (
    select
      manager
    from
      delivery_services
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Pilot Cannot Be Manger!';

end if;

if (
  ip_username not in (
    select
      username
    from
      pilots
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'Invalid Pilot!';

end if;

update
  drones
set
  flown_by = ip_username
where
  (ip_id, ip_tag) = (id, tag);

end / / delimiter;

drop procedure if exists join_swarm;

delimiter / / create procedure join_swarm (
  in ip_id varchar(40),
  in ip_tag integer,
  in ip_swarm_leader_tag integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

#if ((ip_id, ip_swarm_leader_tag) in (select swarm_id, swarm_tag from drones where (ip_id,ip_tag) = (id, tag)))
#then leave sp_main; end if;
if ((ip_id, ip_tag) = (ip_id, ip_swarm_leader_tag)) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The swarm leader should be a different drone!';

end if;

if (
  (ip_id, ip_tag) not in (
    select
      id,
      tag
    from
      drones
  )
  or ip_id not in (
    select
      id
    from
      delivery_services
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone joining the swarm should be valid and owned by the service!';

end if;

if (
  (ip_id, ip_tag) in (
    select
      swarm_id,
      swarm_tag
    from
      drones
    where
      swarm_id is not null
      and swarm_tag is not null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone joining the swarm should not be already leading a swarm!';

end if;

if (
  (ip_id, ip_swarm_leader_tag) not in (
    select
      id,
      tag
    from
      drones
    where
      flown_by is not null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The swarm leader drone should be directly controlled!';

end if;

if (
  (
    select
      hover
    from
      drones
    where
      (id, tag) = (ip_id, ip_tag)
  ) <> (
    select
      hover
    from
      drones
    where
      (id, tag) = (ip_id, ip_swarm_leader_tag)
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drones should be at the same location!';

end if;

if (
  (ip_id, ip_tag) not in (
    select
      id,
      tag
    from
      drones
    where
      flown_by is not null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should be currently being directly controlled by a pilot!';

end if;

update
  drones
set
  swarm_id = ip_id,
  swarm_tag = ip_swarm_leader_tag,
  flown_by = null
where
  (id, tag) =(ip_id, ip_tag);

end / / delimiter;

drop procedure if exists leave_swarm;

delimiter / / create procedure leave_swarm (in ip_id varchar(40), in ip_swarm_tag integer) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  (ip_id, ip_swarm_tag) in (
    select
      swarm_id,
      swarm_tag
    from
      drones
    where
      swarm_id is not null
      and swarm_tag is not null
  )
  or ip_id not in (
    select
      id
    from
      delivery_services
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The selected drone should be owned by the service and flying in a swarm!';

end if;

update
  drones
set
  flown_by = (
    select
      flown_by
    from
      (
        select
          flown_by
        from
          drones
        where
          (id, tag) in (
            select
              swarm_id,
              swarm_tag
            from
              drones
            where
              swarm_id is not null
              and swarm_tag is not null
              and (id, tag) =(ip_id, ip_swarm_tag)
          )
      ) as a
  ),
  swarm_id = null,
  swarm_tag = null
where
  (ip_id, ip_swarm_tag) = (id, tag);

end / / delimiter;

drop procedure if exists load_drone;

delimiter / / create procedure load_drone (
  in ip_id varchar(40),
  in ip_tag integer,
  in ip_barcode varchar(40),
  in ip_more_packages integer,
  in ip_price integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  (ip_id, ip_tag) not in (
    select
      drones.id,
      drones.tag
    from
      delivery_services natural
      join drones
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone being loaded should be owned by the service!';

end if;

if (
  (ip_id, ip_tag) not in (
    select
      id,
      tag
    from
      drones
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone being loaded should be owned by the service!';

end if;

if (
  ip_barcode not in (
    select
      barcode
    from
      ingredients
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The ingredient should be valid!';

end if;

if (
  (ip_id, ip_tag) not in (
    select
      drones.id,
      drones.tag
    from
      delivery_services,
      drones
    where
      drones.hover = delivery_services.home_base
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should be located at the service home base!';

end if;

if (ip_more_packages <= 0) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The quantity of new packages should be greater than zero!';

end if;

if (
  ip_more_packages > (
    select
      capacity - sum(quantity)
    from
      drones,
      payload
    where
      (drones.id, drones.tag) =(payload.id, payload.tag)
      and (drones.id, drones.tag) =(ip_id, ip_tag)
    group by
      payload.id,
      payload.tag
    order by
      payload.id,
      payload.tag
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should have sufficient capacity to carry the new packages!';

end if;

if (
  (ip_id, ip_tag, ip_barcode) in (
    select
      id,
      tag,
      barcode
    from
      payload
  )
) then
update
  payload
set
  quantity = ip_more_packages + (
    select
      quantity
    from
      (
        select
          quantity
        from
          payload
        where
          (ip_id, ip_tag, ip_barcode) =(id, tag, barcode)
      ) as a
  )
where
  (ip_id, ip_tag, ip_barcode) =(id, tag, barcode);

else
insert into
  payload
values
  (
    ip_id,
    ip_tag,
    ip_barcode,
    ip_more_packages,
    ip_price
  );

end if;

end / / delimiter;

drop procedure if exists refuel_drone;

delimiter / / create procedure refuel_drone (
  in ip_id varchar(40),
  in ip_tag integer,
  in ip_more_fuel integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  (ip_id, ip_tag) not in (
    select
      id,
      tag
    from
      drones
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone being switched should be valid and owned by the service!';

end if;

if (
  ip_id not in (
    select
      id
    from
      delivery_services
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone being switched should be valid and owned by the service!';

end if;

if (
  (ip_id, ip_tag) not in (
    select
      drones.id,
      drones.tag
    from
      delivery_services,
      drones
    where
      drones.hover = delivery_services.home_base
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should be located at the service home base!';

end if;

update
  drones
set
  fuel = ip_more_fuel + fuel
where
  (id, tag) = (ip_id, ip_tag);

end / / delimiter;

drop function if exists fuel_required;

delimiter / / create function fuel_required (ip_departure varchar(40), ip_arrival varchar(40)) returns integer reads sql data begin if (ip_departure = ip_arrival) then return 0;

else return (
  select
    1 + truncate(
      sqrt(
        power(arrival.x_coord - departure.x_coord, 2) + power(arrival.y_coord - departure.y_coord, 2)
      ),
      0
    ) as fuel
  from
    (
      select
        x_coord,
        y_coord
      from
        locations
      where
        label = ip_departure
    ) as departure,
    (
      select
        x_coord,
        y_coord
      from
        locations
      where
        label = ip_arrival
    ) as arrival
);

end if;

end / / delimiter;

drop procedure if exists fly_drone;

delimiter / / create procedure fly_drone (
  in ip_id varchar(40),
  in ip_tag integer,
  in ip_destination varchar(40)
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  (ip_id, ip_tag) in (
    select
      id,
      tag
    from
      drones
    where
      flown_by is not null
  )
  and (
    ip_id not in (
      select
        id
      from
        delivery_services
    )
    or ip_id not in (
      select
        id
      from
        pilots
        join work_for on pilots.username = work_for.username
    )
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The lead drone being flown should be directly controlled and owned by the service!';

end if;

if (
  ip_destination not in (
    select
      label
    from
      locations
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The destination should be a validlocation!';

end if;

if (
  ip_destination in (
    select
      hover
    from
      drones
    where
      (ip_id, ip_tag) = (id, tag)
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should not be already at the location!';

end if;

if (
  (
    select
      fuel
    from
      drones
    where
      (ip_id, ip_tag) = (id, tag)
  ) < (
    2 * (
      fuel_required (
        (
          select
            hover
          from
            drones
          where
            (ip_id, ip_tag) = (id, tag)
        ),
        ip_destination
      )
    )
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone/swarm should have enough fuel to reach the destination and (then) home base!';

end if;

if (
  (ip_id, ip_tag) not in (
    select
      swarm_id,
      swarm_tag
    from
      drones
    where
      swarm_id is not null
      and swarm_tag is not null
  )
  and (
    select
      flown_by
    from
      drones
    where
      (ip_id, ip_tag) = (id, tag)
  ) is not null
) ## leader & no others following it ##################################### & not have pilots who control it----
then if (
  (
    (
      select
        space
      from
        locations
      where
        ip_destination = label
    ) - (
      select
        count(*)
      from
        drones
      where
        hover = ip_destination
      group by
        hover
    )
  ) < 1
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone/swarm should have enough space at the destination for the flight!';

end if;

update
  drones
set
  fuel = fuel - (
    fuel_required (
      (
        select
          hover
        from
          (
            select
              hover
            from
              drones
            where
              (ip_id, ip_tag) = (id, tag)
          ) as a
      ),
      ip_destination
    )
  ),
  hover = ip_destination
where
  (ip_id, ip_tag) = (id, tag);

## drone with others whether they are leaders or followers
else if (
  (
    (
      select
        space
      from
        locations
      where
        ip_destination = label
    ) - (
      select
        count(*)
      from
        drones
      where
        hover = ip_destination
      group by
        hover
    )
  ) < (
    select
      count(*) + 1
    from
      drones
    where
      (swarm_id, swarm_tag) = (ip_id, ip_tag)
    group by
      id,
      tag
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone/swarm should have enough space at the destination for the flight!';

end if;

if (
  (
    (
      select
        space
      from
        locations
      where
        ip_destination = label
    ) - (
      select
        count(*)
      from
        drones
      where
        hover = ip_destination
      group by
        hover
    )
  ) < (
    select
      count(*) + 1
    from
      drones
    where
      (swarm_id, swarm_tag) = (
        select
          swarm_id,
          swarm_tag
        from
          drones
        where
          (ip_id, ip_tag) = (id, tag)
          and swarm_id is not null
          and swarm_tag is not null
      )
    group by
      id,
      tag
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone/swarm should have enough space at the destination for the flight!';

end if;

update
  drones
set
  fuel = fuel - (
    fuel_required (
      (
        select
          hover
        from
          (
            select
              hover
            from
              drones
            where
              (ip_id, ip_tag) = (id, tag)
          ) as a
      ),
      ip_destination
    )
  ),
  hover = ip_destination
where
  (ip_id, ip_tag) = (swarm_id, swarm_tag)
  or (ip_id, ip_tag) = (id, tag);

end if;

end / / delimiter;

drop procedure if exists purchase_ingredient;

delimiter / / create procedure purchase_ingredient (
  in ip_long_name varchar(40),
  in ip_id varchar(40),
  in ip_tag integer,
  in ip_barcode varchar(40),
  in ip_quantity integer
) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_long_name not in (
    select
      long_name
    from
      restaurants
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The restaurant should be valid!';

end if;

if (
  (ip_id, ip_tag) not in (
    select
      id,
      tag
    from
      drones
  )
  or (
    select
      hover
    from
      drones
    where
      (ip_id, ip_tag) =(id, tag)
  ) not in (
    select
      location
    from
      restaurants
    where
      long_name = ip_long_name
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should be valid and exist at the location of the resturant!';

end if;

if (
  (
    select
      quantity
    from
      payload
    where
      (ip_id, ip_tag, ip_barcode) = (id, tag, barcode)
  ) < ip_quantity
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should have enough of the requested ingredient!';

end if;

update
  payload
set
  quantity = quantity - ip_quantity
where
  (ip_id, ip_tag, ip_barcode) = (id, tag, barcode);

update
  restaurants
set
  spent = spent + (
    select
      price
    from
      payload
    where
      (ip_id, ip_tag, ip_barcode) = (id, tag, barcode)
  ) * ip_quantity
where
  ip_long_name = long_name;

update
  drones
set
  sales = sales + (
    select
      price
    from
      payload
    where
      (ip_id, ip_tag, ip_barcode) = (id, tag, barcode)
  ) * ip_quantity
where
  (ip_id, ip_tag) = (id, tag);

delete from
  payload
where
  quantity <= 0;

end / / delimiter;

drop procedure if exists remove_ingredient;

delimiter / / create procedure remove_ingredient (in ip_barcode varchar(40)) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_barcode not in (
    select
      barcode
    from
      ingredients
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The ingredient should exist!';

end if;

if (
  ip_barcode in (
    select
      barcode
    from
      payload
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The ingredient should be not being carried by any drones!';

end if;

delete from
  ingredients
where
  barcode = ip_barcode;

end / / delimiter;

drop procedure if exists remove_drone;

delimiter / / create procedure remove_drone (in ip_id varchar(40), in ip_tag integer) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  (ip_id, ip_tag) not in (
    select
      id,
      tag
    from
      drones
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should exist!';

end if;

if (
  (ip_id, ip_tag) in (
    select
      id,
      tag
    from
      payload
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should not be carrying any ingredients!';

end if;

if (
  (ip_id, ip_tag) in (
    select
      swarm_id,
      swarm_tag
    from
      drones
    where
      swarm_id is not null
      and swarm_tag is not null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The drone should not be leading a swarm!';

end if;

delete from
  drones
where
  (ip_id, ip_tag) = (id, tag);

end / / delimiter;

drop procedure if exists remove_pilot_role;

delimiter / / create procedure remove_pilot_role (in ip_username varchar(40)) sp_main: begin DECLARE `negative` CONDITION FOR SQLSTATE '45000';

if (
  ip_username not in (
    select
      username
    from
      pilots
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The pilot should exist!';

end if;

if (
  ip_username in (
    select
      flown_by
    from
      drones
    where
      flown_by is not null
  )
) then SIGNAL `negative`
SET
  MESSAGE_TEXT = 'The pilot should not be controlling any drones!';

end if;

if (
  ip_username in (
    select
      username
    from
      workers
  )
) then
delete from
  pilots
where
  username = ip_username;

else
delete from
  users
where
  username = ip_username;

end if;

end / / delimiter;

create
or replace view display_owner_view as
select
  restaurant_owners.username,
  first_name,
  last_name,
  address,
  count(long_name) as num_restaurants,
  count(distinct location) as num_places,
  COALESCE(max(rating), 0) as highs,
  COALESCE(min(rating), 0) as lows,
  COALESCE(sum(spent), 0) as debt
from
  restaurant_owners
  left join users on (restaurant_owners.username = users.username)
  left join restaurants on (
    restaurant_owners.username = restaurants.funded_by
  )
group by
  username;

create
or replace view display_employee_view as
select
  employees.username,
  taxID,
  salary,
  hired,
  employees.experience as employee_experience,
  COALESCE(licenseID, 'n/a') as licenseID,
  coalesce(pilots.experience, 'n/a') as piloting_experience,
  IF(manager is not null, 'yes', 'no') as manager_status
from
  employees
  left join pilots on (employees.username = pilots.username)
  left join delivery_services on (employees.username = delivery_services.manager);

create
or replace view display_pilot_view as
select
  username,
  licenseID,
  experience,
  sum(num_drone) as num_drones,
  sum(num_location) as num_locations
from
  (
    select
      username,
      licenseID,
      experience,
      count(concat(id, tag)) as num_drone,
      count(distinct hover) as num_location
    from
      pilots
      left join drones on pilots.username = drones.flown_by
    group by
      username
    union
    all
    select
      username,
      licenseID,
      experience,
      count(concat(id, tag)) as num_drone,
      0 as num_location
    from
      drones,
      pilots
    where
      (swarm_id, swarm_tag) in (
        select
          id,
          tag
        from
          drones
        where
          pilots.username = drones.flown_by
      )
    group by
      username
  ) as temp
group by
  username,
  licenseID,
  experience;

create
or replace view display_location_view as
select
  label,
  x_coord,
  y_coord,
  count(distinct restaurants.long_name) as num_restaurants,
  count(distinct delivery_services.id) as num_delivery_services,
  count(distinct concat(drones.id, drones.tag)) as num_drones
from
  locations
  left join restaurants on (restaurants.location = locations.label)
  left join delivery_services on (delivery_services.home_base = locations.label)
  left join drones on (drones.hover = locations.label)
group by
  label;

create
or replace view display_ingredient_view as
select
  iname as ingredient_name,
  drones.hover as location,
  payload.quantity as amount_available,
  min(payload.price) as low_price,
  max(payload.price) as high_price
from
  payload
  join ingredients on ingredients.barcode = payload.barcode
  join drones on (payload.id, payload.tag) = (drones.id, drones.tag)
group by
  ingredient_name,
  hover,
  payload.quantity
order by
  ingredient_name,
  hover;

create
or replace view display_service_view as
select
  delivery_services.id,
  delivery_services.long_name,
  delivery_services.home_base,
  delivery_services.manager,
  sum(distinct drones.sales) as revenue,
  count(distinct payload.barcode) as ingredients_carried,
  sum(payload.quantity * payload.price) as cost_carried,
  sum(payload.quantity * ingredients.weight) as weight_carried
from
  delivery_services
  left join locations on delivery_services.home_base = locations.label
  left join drones on delivery_services.id = drones.id
  left join payload on (drones.id, drones.tag) = (payload.id, payload.tag)
  left join ingredients on payload.barcode = ingredients.barcode
group by
  delivery_services.id,
  delivery_services.long_name,
  delivery_services.home_base,
  delivery_services.manager;