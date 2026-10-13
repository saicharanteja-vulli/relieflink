from pathlib import Path
import json,datetime,csv
P=Path(__file__).resolve().parents[1]; N=50
# Field notation: @db.collection references its record at the same sequence number;
# #integer is a numeric base; ? boolean; ~ choices; plain text is a descriptive label.
specs={
'incidents':('Sai Charan Teja','1258',[
('areas','area_name=Sector|district=~North,South,East,West,Central|state=Demo State|latitude=#17|longitude=#78|population=#2000|household_count=#400|risk_level=~high,medium,low|road_access=~open,restricted|evacuation_zone=Zone'),
('events','area_id=@incidents.areas|event_name=Simulation Event|disaster_type=~flood,cyclone,landslide,earthquake,storm|severity=~high,medium,low|started_at=!0|ended_at=!5|affected_people=#500|response_phase=~response,recovery|lead_agency=Demo Relief Authority|alert_level=~orange,red'),
('alerts','event_id=@incidents.events|area_id=@incidents.areas|alert_type=~evacuation,weather,road_closure|severity=~high,medium|issued_at=!1|expires_at=!2|channel=~sms,radio,public_address|message=Exercise advisory|audience=Residents|acknowledged=?'),
('damage_assessments','event_id=@incidents.events|area_id=@incidents.areas|asset_type=~road,school,bridge,house|asset_name=Assessed asset|damage_level=~minor,moderate,severe|estimated_loss_inr=#100000|assessed_at=!2|assessor_code=Assessor|access_safe=?|repair_priority=~high,medium'),
('situation_reports','event_id=@incidents.events|area_id=@incidents.areas|report_time=!3|affected_households=#100|evacuated_people=#60|roads_blocked=#1|shelters_needed=#1|water_access=~limited,available|power_access=~limited,available|summary=Exercise situation update'),
('weather_observations','event_id=@incidents.events|area_id=@incidents.areas|observed_at=!1|rainfall_mm=#10|wind_kmh=#20|temperature_c=#25|humidity_pct=#40|station_name=Demo station|visibility_km=#1|warning_level=~high,medium,low'),
('hazard_observations','event_id=@incidents.events|area_id=@incidents.areas|observed_at=!1|hazard_type=~debris,standing_water,unstable_structure|severity=~high,medium|observer_code=Observer|location_label=Survey point|estimated_extent_m=#20|verified=?|recommended_action=Restrict access'),
('road_assessments','event_id=@incidents.events|area_id=@incidents.areas|road_name=Relief road|assessed_at=!2|road_condition=~open,restricted,closed|obstruction_type=~debris,water,damage|clearance_hours=#1|vehicle_limit_tonnes=#2|alternate_route=Alternate road|inspection_team=Survey team'),
('agency_updates','event_id=@incidents.events|area_id=@incidents.areas|agency_name=Demo response agency|update_time=!3|resource_type=~boat,ambulance,truck|resources_available=#2|personnel_available=#8|contact_code=Desk|operational_area=Response sector|update_text=Resources ready'),
('recovery_tasks','event_id=@incidents.events|area_id=@incidents.areas|task_name=Recovery task|task_type=~road_clearance,water_restoration,debris_removal|priority=~high,medium|assigned_agency=Demo public works|planned_start=!5|planned_end=!8|budget_inr=#50000|completion_pct=#20')]),
'rescue':('Adithya','1259',[
('teams','team_name=Rescue team|base_area_id=@incidents.areas|specialization=~water,medical,urban|member_count=#6|leader_code=Leader|contact_code=Radio|availability=available|equipment_ready=?|max_people_per_trip=#12|agency=Demo rescue service'),
('vehicles','vehicle_code=Rescue vehicle|vehicle_type=~boat,ambulance,van|team_id=@rescue.teams|seat_capacity=#12|fuel_pct=#50|inspection_at=!-1|service_state=ready|radio_code=Radio|base_area_id=@incidents.areas|operator_code=Operator'),
('requests','event_id=@incidents.events|area_id=@incidents.areas|request_type=~evacuation,medical,search|priority=~high,medium,low|people_count=#2|reported_at=!1|request_state=~assigned,completed|team_id=@rescue.teams|location_label=Pickup point|medical_support=?'),
('dispatches','request_id=@rescue.requests|team_id=@rescue.teams|vehicle_id=@rescue.vehicles|dispatched_at=!1|arrival_at=!2|dispatch_state=arrived|distance_km=#3|dispatcher_code=Dispatcher|radio_channel=Channel|estimated_minutes=#15'),
('evacuations','request_id=@rescue.requests|vehicle_id=@rescue.vehicles|shelter_id=@shelters.shelters|departure_at=!2|arrival_at=!3|people_moved=#2|route_label=Safe route|trip_state=completed|escort_code=Escort|distance_km=#3'),
('search_operations','event_id=@incidents.events|team_id=@rescue.teams|area_id=@incidents.areas|started_at=!1|finished_at=!2|search_method=~ground,boat,drone|searched_buildings=#4|people_located=#2|operation_state=completed|supervisor_code=Supervisor'),
('equipment','team_id=@rescue.teams|equipment_name=Rescue equipment|equipment_type=~rope,life_jacket,stretcher,radio|serial_code=RES|quantity=#2|condition=serviceable|last_checked_at=!-1|next_check_at=!20|storage_label=Team store|supplier=Demo safety supplier'),
('medical_transfers','request_id=@rescue.requests|vehicle_id=@rescue.vehicles|patient_code=Fictional patient|departure_at=!2|arrival_at=!3|destination=Demo care centre|urgency=~urgent,routine|escort_code=Medic|transfer_state=completed|distance_km=#5'),
('mission_logs','team_id=@rescue.teams|request_id=@rescue.requests|logged_at=!3|activity=Rescue exercise completed|people_assisted=#2|hours_worked=#2|fuel_used_litres=#3|safety_issue=false|supervisor_code=Supervisor|outcome=completed'),
('safety_checks','team_id=@rescue.teams|vehicle_id=@rescue.vehicles|checked_at=!-1|checked_by=Safety officer|radio_ok=true|first_aid_ok=true|fuel_ok=true|ppe_ok=true|check_result=pass|next_check_at=!10')]),
'shelters':('Sreedhar','1260',[
('shelters','area_id=@incidents.areas|shelter_name=Relief shelter|building_type=~school,hall,community_centre|capacity_people=#100|water_litres=#1000|toilet_count=#10|accessible=true|manager_code=Manager|opened_at=!1|shelter_state=open'),
('households','event_id=@incidents.events|origin_area_id=@incidents.areas|household_code=Fictional household|member_count=#2|children_count=1|adults_count=#1|preferred_language=~Telugu,Hindi,English|accessibility_needed=?|registered_at=!2|contact_token=Household desk token'),
('admissions','shelter_id=@shelters.shelters|household_id=@shelters.households|admitted_at=!3|people_admitted=#2|assigned_zone=Zone A|admission_state=active|admitted_by=Registrar|bedding_issued=true|meal_plan=standard|expected_departure=!10'),
('bed_allocations','shelter_id=@shelters.shelters|admission_id=@shelters.admissions|room_label=Dormitory|bed_start=#1|beds_allocated=#2|allocated_at=!3|allocation_state=occupied|accessible_bed=?|allocated_by=Registrar|floor_number=0'),
('meal_services','shelter_id=@shelters.shelters|served_at=!4|meal_type=~breakfast,lunch,dinner|portions_prepared=#50|portions_served=#40|menu=Rice and vegetables|provider=Demo kitchen|allergen_note=Check ingredients|supervisor_code=Kitchen lead|food_check=passed'),
('supply_requests','shelter_id=@shelters.shelters|requested_at=!3|item_name=~blanket,water,soap|quantity_requested=#20|unit=units|priority=~high,medium|request_state=approved|required_by=!4|requested_by=Manager|purpose=Resident support'),
('health_visits','shelter_id=@shelters.shelters|household_id=@shelters.households|visited_at=!4|clinician_code=Demo clinician|visit_type=Routine screening|people_seen=#2|followup_needed=?|followup_at=!5|visit_state=completed|notes=Fictional wellness visit'),
('sanitation_checks','shelter_id=@shelters.shelters|checked_at=!4|inspector_code=Inspector|water_safe=true|toilets_clean=true|waste_collected=true|soap_available=true|check_result=pass|next_check_at=!5|notes=Routine exercise inspection'),
('occupancy_snapshots','shelter_id=@shelters.shelters|recorded_at=!4|people_present=#2|households_present=1|beds_occupied=#2|capacity_people=#100|available_places=CALC|recorded_by=Manager|snapshot_type=daily|verified=true'),
('feedback_cases','shelter_id=@shelters.shelters|household_id=@shelters.households|submitted_at=!4|category=~food,water,bedding|priority=~low,medium|description=Exercise service feedback|case_state=open|assigned_to=Manager|target_resolution=!6|channel=help_desk')]),
'logistics':('Divya','1261',[
('warehouses','area_id=@incidents.areas|warehouse_name=Relief warehouse|capacity_units=#10000|manager_code=Store manager|contact_code=Warehouse desk|storage_type=ambient|loading_bays=#2|power_backup=true|inspection_at=!-1|warehouse_state=active'),
('items','item_name=Relief item|category=~food,water,hygiene,bedding,medical|unit=units|unit_weight_kg=#1|reorder_level=#20|shelf_life_days=#180|storage_condition=dry|supplier_code=Demo supplier|pack_size=#1|essential=true'),
('stock_batches','warehouse_id=@logistics.warehouses|item_id=@logistics.items|batch_code=Batch|received_at=!1|expires_at=!180|quantity_received=#200|quantity_available=CALC|unit_cost_inr=#100|quality_state=accepted|bin_label=Bin'),
('suppliers','supplier_name=Demo supplier|area_id=@incidents.areas|category=~food,water,hygiene,bedding,medical|contact_token=Supplier desk|lead_time_days=#1|rating=#1|active=true|payment_terms=30 days|registered_at=!-20|delivery_radius_km=#50'),
('purchase_orders','supplier_id=@logistics.suppliers|item_id=@logistics.items|warehouse_id=@logistics.warehouses|ordered_at=!-2|expected_at=!1|quantity=#200|unit_price_inr=#100|total_inr=CALC|order_state=received|approved_by=Procurement officer'),
('shipments','batch_id=@logistics.stock_batches|warehouse_id=@logistics.warehouses|shelter_id=@shelters.shelters|dispatched_at=!2|delivered_at=!3|quantity=#20|carrier=Demo relief carrier|tracking_code=Shipment|shipment_state=delivered|unit=units'),
('delivery_receipts','shipment_id=@logistics.shipments|received_at=!3|received_by=Shelter manager|quantity_received=#20|quantity_damaged=0|receipt_state=accepted|proof_code=Receipt|condition=dry|checked_by=Store assistant|remarks=Exercise delivery accepted'),
('stock_movements','batch_id=@logistics.stock_batches|shipment_id=@logistics.shipments|movement_type=outbound|quantity=#20|moved_at=!2|authorized_by=Store manager|handled_by=Store assistant|source_bin=Bin|destination_type=shelter|movement_state=posted'),
('quality_inspections','batch_id=@logistics.stock_batches|inspected_at=!1|inspector_code=Quality inspector|sample_units=#2|packaging_ok=true|expiry_ok=true|contamination_found=false|inspection_result=pass|action=release|notes=Exercise quality check'),
('transport_runs','shipment_id=@logistics.shipments|vehicle_code=Logistics truck|driver_code=Demo driver|departed_at=!2|arrived_at=!3|distance_km=#20|fuel_litres=#5|route_label=Relief corridor|run_state=completed|load_units=#20')]),
'volunteers':('Harsha','1262',[
('profiles','display_name=Demo volunteer|home_area_id=@incidents.areas|age=#20|language=~Telugu,Hindi,English|primary_skill=~first_aid,driving,logistics|experience_months=#6|contact_token=Volunteer desk|joined_at=!-30|available=true|preferred_shift=day'),
('skill_records','volunteer_id=@volunteers.profiles|skill_name=~first_aid,driving,logistics|proficiency=~basic,intermediate,advanced|assessed_at=!-10|assessor_code=Trainer|verified=true|practice_hours=#10|assessment_score=#60|valid_until=!300|evidence_code=Skill record'),
('training_sessions','session_name=Relief training|topic=~first_aid,logistics,safety|trainer_code=Trainer|area_id=@incidents.areas|starts_at=!-15|ends_at=!-14|capacity=#30|duration_hours=#2|delivery_mode=in_person|session_state=completed'),
('training_enrollments','volunteer_id=@volunteers.profiles|session_id=@volunteers.training_sessions|enrolled_at=!-20|attendance_state=attended|score=#60|passed=true|certificate_code=Certificate|completed_at=!-14|feedback_score=#1|enrollment_state=completed'),
('availability_slots','volunteer_id=@volunteers.profiles|area_id=@incidents.areas|starts_at=!1|ends_at=!2|shift_type=day|available_hours=#4|travel_radius_km=#10|transport_available=?|slot_state=available|recorded_at=!0'),
('assignments','volunteer_id=@volunteers.profiles|event_id=@incidents.events|shelter_id=@shelters.shelters|assigned_at=!1|starts_at=!3|ends_at=!4|role=~registration,distribution,sanitation|assignment_state=completed|supervisor_code=Coordinator|hours_planned=24'),
('attendance','volunteer_id=@volunteers.profiles|assignment_id=@volunteers.assignments|check_in=!3|check_out=!4|hours_worked=24|attendance_state=present|verified_by=Coordinator|break_minutes=0|site_type=shelter|remarks=Exercise shift record'),
('certifications','volunteer_id=@volunteers.profiles|certification_name=Relief safety orientation|issuer=Demo training centre|issued_at=!-10|expires_at=!300|certificate_code=Credential|verification_state=verified|level=basic|training_hours=#8|renewal_required=true'),
('reimbursements','volunteer_id=@volunteers.profiles|assignment_id=@volunteers.assignments|claimed_at=!5|expense_type=travel|amount_inr=#200|currency=INR|claim_state=approved|approved_by=Coordinator|receipt_code=Travel receipt|paid_at=!6'),
('performance_reviews','volunteer_id=@volunteers.profiles|assignment_id=@volunteers.assignments|reviewed_at=!5|reviewer_code=Coordinator|punctuality_score=#1|teamwork_score=#1|safety_score=#1|hours_confirmed=24|feedback=Exercise completed safely|eligible_for_reassignment=true')]),
'donations':('Mounica Sai','1267',[
('donors','donor_name=Demo donor|donor_type=~individual,company,foundation|area_id=@incidents.areas|contact_token=Donor desk|preferred_cause=disaster_relief|registered_at=!-20|anonymous=?|receipt_preference=digital|active=true|consent_recorded=true'),
('campaigns','event_id=@incidents.events|campaign_name=Relief appeal|started_at=!0|ends_at=!20|target_inr=#100000|currency=INR|organizer=Demo relief trust|campaign_state=active|purpose=Shelter supplies|public_code=Appeal'),
('pledges','donor_id=@donations.donors|campaign_id=@donations.campaigns|pledged_at=!1|amount_inr=#10000|currency=INR|due_at=!2|pledge_state=fulfilled|payment_method=bank_transfer|reference_code=Pledge|restricted_purpose=relief_supplies'),
('donations','donor_id=@donations.donors|campaign_id=@donations.campaigns|pledge_id=@donations.pledges|received_at=!2|amount_inr=#10000|currency=INR|payment_method=bank_transfer|payment_reference=Payment|donation_state=received|restricted_purpose=relief_supplies'),
('receipts','donation_id=@donations.donations|donor_id=@donations.donors|issued_at=!2|receipt_number=Donation receipt|amount_inr=#10000|currency=INR|issued_by=Finance officer|delivery_method=digital|receipt_state=issued|acknowledgment=Exercise donation acknowledgment'),
('allocations','donation_id=@donations.donations|event_id=@incidents.events|allocated_at=!3|amount_inr=#5000|currency=INR|purpose=relief_supplies|approved_by=Finance lead|allocation_state=approved|beneficiary_area_id=@incidents.areas|reference_code=Allocation'),
('expenses','allocation_id=@donations.allocations|spent_at=!4|amount_inr=#3000|currency=INR|category=relief_supplies|vendor=Demo relief vendor|invoice_code=Invoice|approved_by=Finance lead|expense_state=paid|description=Exercise relief kits'),
('beneficiary_groups','event_id=@incidents.events|area_id=@incidents.areas|group_name=Demo beneficiary group|household_count=#5|people_count=#20|need_category=~food,hygiene,bedding|registered_at=!2|verified_by=Field officer|verification_state=verified|contact_token=Group representative'),
('distributions','beneficiary_group_id=@donations.beneficiary_groups|expense_id=@donations.expenses|distributed_at=!5|item_description=Relief kit|quantity=#20|unit=kits|distributed_by=Field officer|acknowledgment_code=Distribution proof|distribution_state=completed|location_label=Community point'),
('audit_checks','donation_id=@donations.donations|allocation_id=@donations.allocations|expense_id=@donations.expenses|checked_at=!6|auditor_code=Demo auditor|receipt_verified=true|allocation_verified=true|expense_verified=true|check_result=pass|notes=Exercise traceability check')])}

def rid(db,c,i):return f'{db[:3].upper()}-{c.upper()}-{i:03d}'
def date(i,offset):return (datetime.datetime(2026,1,1,tzinfo=datetime.timezone.utc)+datetime.timedelta(days=i*3+offset)).isoformat().replace('+00:00','Z')
def value(v,i):
 if v.startswith('@'):
  d,c=v[1:].split('.');return rid(d,c,i)
 if v.startswith('#'):return int(v[1:])+i%5
 if v.startswith('!'):return {'$date':date(i,int(v[1:]))}
 if v.startswith('~'):a=v[1:].split(',');return a[(i-1)%len(a)]
 if v=='?':return i%2==0
 if v in ('true','false'):return v=='true'
 if v.isdigit():return int(v)
 return v if v in ('INR','units','active','available','completed','pass','verified','received','approved','paid','dry','ambient','standard','day','open','occupied','assigned','arrived','accepted','delivered','posted','outbound','shelter','in_person','present','basic','digital','issued','bank_transfer','fulfilled','relief_supplies','kits','disaster_relief','response','ready','serviceable','release') else f'{v} {i:03d}'
manifest={'project':'ReliefLink','synthetic':True,'records_per_collection':N,'databases':[]}; data={}; refs=[]
for db,(member,roll,cols) in specs.items():
 dbname='relieflink_'+db; entry={'name':dbname,'key':db,'member':member,'roll':roll,'collections':[]}; (P/'data'/dbname).mkdir(parents=True,exist_ok=True)
 for c,fields in cols:
  defs=dict(f.split('=',1) for f in fields.split('|'));docs=[]
  for i in range(1,N+1):
   doc={'_id':rid(db,c,i),**{k:value(v,i) for k,v in defs.items()},'created_at':{'$date':date(i,-40)},'updated_at':{'$date':date(i,10)},'data_source':'synthetic_academic','record_version':1}
   if c=='occupancy_snapshots':doc['available_places']=doc['capacity_people']-doc['people_present']
   if c=='stock_batches':doc['quantity_available']=doc['quantity_received']-(20+i%5)
   if c=='purchase_orders':doc['total_inr']=doc['quantity']*doc['unit_price_inr']
   if c=='profiles':doc['age']=20+i%30
   docs.append(doc)
  data[(db,c)]=docs
  schema={'bsonType':'object','required':list(docs[0]),'additionalProperties':False,'properties':{}}
  for k,v in docs[0].items():
   t='date' if isinstance(v,dict) and '$date' in v else 'bool' if isinstance(v,bool) else ['int','long','double','decimal'] if isinstance(v,(int,float)) else 'string'
   prop={'bsonType':t}
   if isinstance(v,(int,float)) and not isinstance(v,bool):prop['minimum']=0
   if k in defs and defs[k].startswith('~'):prop['enum']=defs[k][1:].split(',')
   schema['properties'][k]=prop
  localrefs=[]
  for k,v in defs.items():
   if v.startswith('@'):
    d,co=v[1:].split('.');r={'field':k,'database':'relieflink_'+d,'collection':co};localrefs.append(r);refs.append((db,c,k,d,co))
  entry['collections'].append({'name':c,'count':N,'domain_fields':len(defs),'fields':list(docs[0]),'schema':schema,'references':localrefs})
  (P/'data'/dbname/(c+'.json')).write_text(json.dumps(docs,indent=2))
 manifest['databases'].append(entry)
(P/'manifest.json').write_text(json.dumps(manifest,indent=2))
for db,c,k,d,co in refs:
 ids={x['_id'] for x in data[d,co]};assert all(x[k] in ids for x in data[db,c])
assert len(data)==60 and all(len(d)==50 and all(len(x)-1>=10 for x in d) for d in data.values())
print('Generated 6 databases, 60 collections, 3000 documents; references valid.')
with (P/'docs'/'Collection_Checklist.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['Member','Roll','Database','Collection','Documents','Fields excluding _id'])
 for db in manifest['databases']:
  for c in db['collections']:w.writerow([db['member'],db['roll'],db['name'],c['name'],50,len(c['fields'])-1])
