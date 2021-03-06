from header import *

#script_player_arrived
# Called in start_phase_3 game_menus. 
# INPUT: none
# OUTPUT: none
player_arrived = (
	"player_arrived",
		[
			(assign, ":player_faction_culture", "fac_culture_western"),
			(faction_set_slot, "fac_player_supporters_faction",  slot_faction_culture, ":player_faction_culture"),
			(faction_set_slot, "fac_player_faction",  slot_faction_culture, ":player_faction_culture"),
	])

# script_game_event_party_encounter:
# This script is called from the game engine whenever player party encounters another party or a battle on the world map
# INPUT: param1: encountered_party, param2: second encountered_party (if this was a battle)
# OUTPUT: none
game_event_party_encounter = (
	"game_event_party_encounter",
		[
			(store_script_param_1, "$g_encountered_party"),
			(store_script_param_2, "$g_encountered_party_2"),# encountered_party2 is set when we come across a battle or siege, otherwise it's a negative value
			#       (store_encountered_party, "$g_encountered_party"),
			#       (store_encountered_party2,"$g_encountered_party_2"), # encountered_party2 is set when we come across a battle or siege, otherwise it's a minus value
			(store_faction_of_party, "$g_encountered_party_faction","$g_encountered_party"),
			(store_relation, "$g_encountered_party_relation", "$g_encountered_party_faction", "fac_player_faction"),
			
			(party_get_slot, "$g_encountered_party_type", "$g_encountered_party", slot_party_type),
			(party_get_template_id,"$g_encountered_party_template","$g_encountered_party"),
			#       (try_begin),
			#         (gt, "$g_encountered_party_2", 0),
			#         (store_faction_of_party, "$g_encountered_party_2_faction","$g_encountered_party_2"),
			#         (store_relation, "$g_encountered_party_2_relation", "$g_encountered_party_2_faction", "fac_player_faction"),
			#         (party_get_template_id,"$g_encountered_party_2_template","$g_encountered_party_2"),
			#       (else_try),
			#         (assign, "$g_encountered_party_2_faction",-1),
			#         (assign, "$g_encountered_party_2_relation", 0),
			#         (assign,"$g_encountered_party_2_template", -1),
			#       (try_end),
			
			#NPC companion changes begin
			(call_script, "script_party_count_fit_regulars", "p_main_party"),
			(assign, "$playerparty_prebattle_regulars", reg0),
			
			#        (try_begin),
			#            (assign, "$player_party__regulars", 0),
			#            (call_script, "script_party_count_fit_regulars", "p_main_party"),
			#            (gt, reg0, 0),
			#            (assign, "$player_party_contains_regulars", 1),
			#        (try_end),
			#NPC companion changes end
		##tom rebalance
			(try_begin), 
			(eq, "$culture_pool_initialized", 1),
		(eq, "$culture_pool", 1),
		(call_script, "script_rebalance_troops_by_culture"),
		(try_end),
		##tom rebalance
			
			(assign, "$g_last_rest_center", -1),
			(assign, "$talk_context", 0),
			(assign,"$g_player_surrenders",0),
			(assign,"$g_enemy_surrenders",0),
			(assign, "$g_leave_encounter",0),
			(assign, "$g_engaged_enemy", 0),
			#       (assign,"$waiting_for_arena_fight_result", 0),
			#       (assign,"$arena_bet_amount",0),
			#       (assign,"$g_player_raiding_village",0),
			(try_begin),
				(neg|is_between, "$g_encountered_party", centers_begin, centers_end),
				(rest_for_hours, 0), #stop waiting
				(assign, "$g_infinite_camping", 0),
			(try_end),
			#       (assign, "$g_permitted_to_center",0),
			(assign, "$new_encounter", 1), #check this in the menu.
			(try_begin),
				(lt, "$g_encountered_party_2",0), #Normal encounter. Not battle or siege.
				(try_begin),
					(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
					(jump_to_menu, "mnu_castle_outside"),
				(else_try),
					(party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
					(jump_to_menu, "mnu_castle_outside"),
				(else_try),
					(party_slot_eq, "$g_encountered_party", slot_party_type, spt_ship),
					(jump_to_menu, "mnu_ship_reembark"),
				(else_try),
					(party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
					(jump_to_menu, "mnu_village"),
				(else_try),
					(party_slot_eq, "$g_encountered_party", slot_party_type, spt_cattle_herd),
					(jump_to_menu, "mnu_cattle_herd"),
				(else_try),
					(is_between, "$g_encountered_party", training_grounds_begin, training_grounds_end),
					(jump_to_menu, "mnu_training_ground"),
				(else_try),
					(party_get_template_id, ":template", "$g_encountered_party"),
					(ge, ":template", "pt_steppe_bandit_lair"),
					(lt, ":template", "pt_bandit_lair_templates_end"),
					(assign, "$loot_screen_shown", 0),
					#		   (call_script, "script_encounter_init_variables"),
					(jump_to_menu, "mnu_bandit_lair"),
				(else_try),
					(eq, "$g_encountered_party", "p_zendar"),
					(jump_to_menu, "mnu_zendar"),
				(else_try),
					(eq, "$g_encountered_party", "p_salt_mine"),
					(jump_to_menu, "mnu_salt_mine"),
				(else_try),
					(eq, "$g_encountered_party", "p_four_ways_inn"),
					(jump_to_menu, "mnu_four_ways_inn"),
				(else_try),
					(eq, "$g_encountered_party", "p_test_scene"),
					(jump_to_menu, "mnu_test_scene"),
				(else_try),
					(eq, "$g_encountered_party", "p_battlefields"),
					(jump_to_menu, "mnu_battlefields"),
				(else_try),
					(eq, "$g_encountered_party", "p_training_ground"),
					(jump_to_menu, "mnu_tutorial"),
				(else_try),
					(eq, "$g_encountered_party", "p_camp_bandits"),
					(jump_to_menu, "mnu_camp"),
		(else_try), #tom - manor
					(eq, "$g_encountered_party_template", "pt_manor"),
			(jump_to_menu, "mnu_manor_center"),
		(else_try),
			(party_slot_eq, "$g_encountered_party", slot_mongol_camp_status, status_stationed),
			(eq, "$g_encountered_party_template", "pt_mongolian_camp"),
			(jump_to_menu, "mnu_mongol_camp"),
			#tom end	
				(else_try),
					# (try_begin),
					# (lt, "$g_encountered_party_relation", 0),
					# (party_slot_eq, "$g_encountered_party", slot_party_type, spt_kingdom_hero_party),
					# (try_begin),
					# (eq, "$g_battle_preparation_phase", 0),
					# (assign, "$g_battle_preparation_phase", 1),
					# (try_end),
					# (try_end),
					(jump_to_menu, "mnu_simple_encounter"),
				(try_end),
			(else_try), #Battle or siege
				(try_begin),
					(this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
					(party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
					(try_begin),
						(eq, "$auto_enter_town", "$g_encountered_party"),
						(jump_to_menu, "mnu_town"),
					(else_try),
						(eq, "$auto_besiege_town", "$g_encountered_party"),
						(jump_to_menu, "mnu_besiegers_camp_with_allies"),
					(else_try),
						(jump_to_menu, "mnu_join_siege_outside"),
					(try_end),
				(else_try),
					(jump_to_menu, "mnu_pre_join"),
				(try_end),
			(try_end),
			(assign,"$auto_enter_town",0),
			(assign,"$auto_besiege_town",0),
	])

		# script_process_village_raids
		# called from triggers every two hours
		# WARNING: modified by 1257AD devs
		# Input: none
		# Output: none
process_village_raids = (
	"process_village_raids",
			[
				(try_for_range, ":village_no", villages_begin, villages_end),
					(party_get_slot, ":village_raid_progress", ":village_no", slot_village_raid_progress),
					(try_begin),
						(party_slot_eq, ":village_no", slot_village_state, 0), #village is normal
						(val_sub, ":village_raid_progress", 5),
						(val_max, ":village_raid_progress", 0),
						(party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
						(try_begin),
							(lt, ":village_raid_progress", 50),
							
							# (try_begin),
								# (party_get_icon, ":village_icon", ":village_no"),
								# (neq, ":village_icon", "icon_village_a"),
								# (party_set_icon, ":village_no", "icon_village_a"),
							# (try_end),
							
							(party_slot_ge, ":village_no", slot_village_smoke_added, 1),
							(party_set_slot, ":village_no", slot_village_smoke_added, 0),
							(party_clear_particle_systems, ":village_no"),
						(try_end),
					(else_try),
						(party_slot_eq, ":village_no", slot_village_state, svs_being_raided), #village is being raided
						#End raid unless there is an enemy party nearby
						(assign, ":raid_ended", 1),
						(party_get_slot, ":raider_party", ":village_no", slot_village_raided_by),
						
						(try_begin),
							(ge, ":raider_party", 0),
							(party_is_active, ":raider_party"),
							(this_or_next|neq, ":raider_party", "p_main_party"),
							(eq, "$g_player_is_captive", 0),
							(store_distance_to_party_from_party, ":distance", ":village_no", ":raider_party"),
							(lt, ":distance", raid_distance),
							(assign, ":raid_ended", 0),
						(try_end),
						
						(try_begin),
							(eq, ":raid_ended", 1),
							(call_script, "script_village_set_state", ":village_no", svs_normal), #clear raid flag
							(party_set_slot, ":village_no", slot_village_smoke_added, 0),
							(party_clear_particle_systems, ":village_no"),
						(else_try),
							(assign, ":raid_progress_increase", 11),
							(party_get_slot, ":looter_party", ":village_no", slot_village_raided_by),
							(try_begin),
								(party_get_skill_level, ":looting_skill", ":looter_party", "skl_looting"),
								(val_add, ":raid_progress_increase", ":looting_skill"),
							(try_end),
							(try_begin),
								(party_slot_eq, ":village_no", slot_center_has_watch_tower, 1),
								(val_mul, ":raid_progress_increase", 2),
								(val_div, ":raid_progress_increase", 3),
							(try_end),
							(val_add, ":village_raid_progress", ":raid_progress_increase"),
							(party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
							(try_begin),
								(ge, ":village_raid_progress", 50),
								(party_slot_eq, ":village_no", slot_village_smoke_added, 0),
								(party_add_particle_system, ":village_no", "psys_map_village_fire"),
								(party_add_particle_system, ":village_no", "psys_map_village_fire_smoke"),
								#(party_set_icon, ":village_no", "icon_village_burnt_a"), #tom
								(party_set_slot, ":village_no", slot_village_smoke_added, 1),
							(try_end),
							(try_begin),
								(gt, ":village_raid_progress", 100),
								(str_store_party_name_link, s1, ":village_no"),
								(party_stack_get_troop_id, ":raid_leader", ":looter_party", 0),
								(ge, ":raid_leader", 0),
								(str_store_party_name, s2, ":looter_party"),
								# rafi
								(store_troop_faction, ":troop_faction", ":raid_leader"),
								(store_relation, ":rel", ":troop_faction", "$players_kingdom"),
								(try_begin),
									(this_or_next | lt, ":rel", 0),
									(eq, ":troop_faction", "$players_kingdom"),
									(display_log_message, "@The village of {s1} has been looted by {s2}."),
								(try_end),
								# end rafi
								
								(try_begin),
									(party_get_slot, ":village_lord", ":village_no", slot_town_lord),
									(is_between, ":village_lord", active_npcs_begin, active_npcs_end),
									(call_script, "script_troop_change_relation_with_troop", ":raid_leader", ":village_lord", -1),
									(val_add, "$total_battle_enemy_changes", -1),
								(try_end),
								
								#give loot gold to raid leader
								(troop_get_slot, ":raid_leader_gold", ":raid_leader", slot_troop_wealth),
								(party_get_slot, ":village_prosperity", ":village_no"),
								(store_mul, ":value_of_loot", ":village_prosperity", 60), #average is 3000
								(val_add, ":raid_leader_gold", ":value_of_loot"),
								(troop_set_slot, ":raid_leader", slot_troop_wealth, ":raid_leader_gold"),
								
								#take loot gold from village lord #new 1.126
								(try_begin),
									(is_between, ":village_lord", active_npcs_begin, active_npcs_end),
									(troop_get_slot, ":village_lord_gold", ":village_lord", slot_troop_wealth),
									(val_sub, ":village_lord_gold", ":value_of_loot"),
									(val_max, ":village_lord_gold", 0),
									(troop_set_slot, ":village_lord", slot_troop_wealth, ":village_lord_gold"),
								(try_end),
								
								(call_script, "script_village_set_state",  ":village_no", svs_looted),
								(party_set_slot, ":village_no", slot_center_accumulated_rents, 0), #new 1.126
								(party_set_slot, ":village_no", slot_center_accumulated_tariffs, 0), #new 1.126
								
								(party_set_slot, ":village_no", slot_village_raid_progress, 0),
								(party_set_slot, ":village_no", slot_village_recover_progress, 0),
								(try_begin),
									(store_faction_of_party, ":village_faction", ":village_no"),
									(this_or_next|party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
									(eq, ":village_faction", "fac_player_supporters_faction"),
									(call_script, "script_add_notification_menu", "mnu_notification_village_raided", ":village_no", ":raid_leader"),
								(try_end),
								(call_script, "script_add_log_entry", logent_village_raided, ":raid_leader",  ":village_no", -1, -1),
								(store_faction_of_party, ":looter_faction", ":looter_party"),
								#(call_script, "script_faction_inflict_war_damage_on_faction", ":looter_faction", ":village_faction", 5),
								(call_script, "script_faction_inflict_war_damage_on_faction", ":looter_faction", ":village_faction", 15), # rafi
							(try_end),
						(try_end),
					(else_try),
						(party_slot_eq, ":village_no", slot_village_state, svs_looted), #village is looted
						(party_get_slot, ":recover_progress", ":village_no", slot_village_recover_progress),
						(val_add, ":recover_progress", 1),
						(party_set_slot, ":village_no", slot_village_recover_progress, ":recover_progress"), #village looted
						(try_begin),
							(ge, ":recover_progress", 10),
							(party_slot_eq, ":village_no", slot_village_smoke_added, 1),
							(party_clear_particle_systems, ":village_no"),
							(party_add_particle_system, ":village_no", "psys_map_village_looted_smoke"),
							(party_set_slot, ":village_no", slot_village_smoke_added, 2),
						(try_end),
						(try_begin),
							(gt, ":recover_progress", 50),
							(party_slot_eq, ":village_no", slot_village_smoke_added, 2),
							(party_clear_particle_systems, ":village_no"),
							(party_set_slot, ":village_no", slot_village_smoke_added, 3),
							#(party_set_icon, ":village_no", "icon_village_deserted_a"),
						(try_end),
						(try_begin),
							(gt, ":recover_progress", 100),
							(call_script, "script_village_set_state",  ":village_no", 0),#village back to normal
							(party_set_slot, ":village_no", slot_village_recover_progress, 0),
							(party_clear_particle_systems, ":village_no"),
							(party_set_slot, ":village_no", slot_village_smoke_added, 0),
							#(party_set_icon, ":village_no", "icon_village_a"),
						(try_end),
					(try_end),
				(try_end),
		])
		
		## campaign
		# script_process_sieges
		# called from triggers
		# WARNING: heavily modified by 1257AD devs
		# Input: none
		# Output: none
process_sieges = (
	"process_sieges",
			[
				(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
					#Reducing siege hardness every day by 20
					(party_get_slot, ":siege_hardness", ":center_no", slot_center_siege_hardness),
					(val_sub, ":siege_hardness", 20),
					(val_max, ":siege_hardness", 0),
					(party_set_slot, ":center_no", slot_center_siege_hardness, ":siege_hardness"),
					
					(party_get_slot, ":town_food_store", ":center_no", slot_party_food_store),
					(call_script, "script_center_get_food_store_limit", ":center_no"),
					(assign, ":food_store_limit", reg0),
					(try_begin),
						(party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
						(ge, ":besieger_party", 0), #town is under siege
						
					#Reduce prosperity of besieged castle/town by -0.33/-4 every day.
					 (try_begin),
						 (try_begin),
							 (is_between, ":center_no", castles_begin, castles_end),
							 (store_random_in_range, ":random_value", 0, 3),
							 (try_begin),
								 (eq, ":random_value", 0),
								 (assign, ":daily_siege_effect_on_prosperity", -1),
							 (else_try),
								 (assign, ":daily_siege_effect_on_prosperity", 0),
							 (try_end),
						 (else_try),
							 (assign, ":daily_siege_effect_on_prosperity", -4),
						 (try_end),
			 
						 (call_script, "script_change_center_prosperity", ":center_no", ":daily_siege_effect_on_prosperity"),
						 (val_add, "$newglob_total_prosperity_from_townloot", ":daily_siege_effect_on_prosperity"),
					 (try_end),
						
						(store_faction_of_party, ":center_faction", ":center_no"),
						# Lift siege unless there is an enemy party nearby
						(assign, ":siege_lifted", 0),
						(try_begin),
							(try_begin),
								(neg|party_is_active, ":besieger_party"),
								(assign, ":siege_lifted", 1),
							(else_try),
								(store_distance_to_party_from_party, ":besieger_distance", ":center_no", ":besieger_party"),
								(gt, ":besieger_distance", 5),
								(assign, ":siege_lifted", 1),
							(else_try),
								##diplomacy begin
								(neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
								##diplomacy end
								(store_faction_of_party, ":besieger_faction", ":besieger_party"),
								(store_relation, ":reln", ":besieger_faction", ":center_faction"),
								(ge, ":reln", 0),
								(assign, ":siege_lifted", 1),
							(try_end),
							
							
							(eq, ":siege_lifted", 1),
							#If another lord can take over the siege, it isn't lifted
							(try_for_range, ":enemy_hero", active_npcs_begin, active_npcs_end),
								(troop_slot_eq, ":enemy_hero", slot_troop_occupation, slto_kingdom_hero),
								(troop_get_slot, ":enemy_party", ":enemy_hero", slot_troop_leaded_party),
								(ge, ":enemy_party", 0),
								(party_is_active, ":enemy_party"),
								(store_faction_of_party, ":party_faction", ":enemy_party"),
								(store_relation, ":reln", ":party_faction", ":center_faction"),
								(lt, ":reln", 0),
								(store_distance_to_party_from_party, ":distance", ":center_no", ":enemy_party"),
								(lt, ":distance", 4),
								(assign, ":besieger_party", ":enemy_party"),
								(party_set_slot, ":center_no", slot_center_is_besieged_by, ":enemy_party"),
								(assign, ":siege_lifted", 0),
							(try_end),
						(try_end),
						(try_begin),
							(eq, ":siege_lifted", 1),
							(call_script, "script_lift_siege", ":center_no", 1),
						(else_try),
							(call_script, "script_center_get_food_consumption", ":center_no"),
							(assign, ":food_consumption", reg0),
							(val_sub, ":town_food_store", ":food_consumption"), # reduce food only under siege???
							(try_begin),
								(le, ":town_food_store", 0), #town is starving
								
								# rafi - cause casualties if no food
								# (party_get_num_companion_stacks, ":num_stacks", ":center_no"),
								# (try_for_range, ":stack_no", 0, ":num_stacks"),
									# (party_stack_get_troop_id, ":stack_troop", ":center_no", ":stack_no"),
									# (try_begin),
										# (party_stack_get_size, ":stack_size", ":center_no", ":stack_no"),
										# (gt, ":stack_size", 0),
										# (store_div, ":to_remove", ":stack_size", 10),
										# (party_remove_members, ":center_no", ":stack_troop", ":to_remove"),
										
										# (party_stack_get_size, ":stack_size", ":center_no", ":stack_no"),
										# (gt, ":stack_size", 0),
										# (store_random_in_range, ":random", 1, ":stack_size"),
										# (party_wound_members, ":center_no", ":stack_troop", ":random"),
									# (try_end),
								# (try_end),
								# end rafi
								(store_random_in_range, ":r", 0, 10),
								(gt, ":r", 0),
								(call_script, "script_party_inflict_attrition", ":center_no", ":r"), #tom
								
								# (store_random_in_range, ":r", 0, 100),
								# (lt, ":r", 10),
								# (call_script, "script_party_wound_all_members", ":center_no"), # town falls with 10% chance if starving
							(try_end),
						(try_end),
					(else_try),
						#town is not under siege...
						(val_add, ":town_food_store", 30), #add 30 food (significant for castles only.
					(try_end),
					
					(val_min, ":town_food_store", ":food_store_limit"),
					(val_max, ":town_food_store", 0),
					(party_set_slot, ":center_no", slot_party_food_store, ":town_food_store"),
				(try_end),
		])

# script_allow_vassals_to_join_indoor_battle
		# Input: none
		# Output: none
allow_vassals_to_join_indoor_battle = (
	"allow_vassals_to_join_indoor_battle",
			[
				#if our commander attacks an enemy army
				(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
					(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
					(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
					(gt, ":party_no", 0),
					(party_is_active, ":party_no"),
					
					(party_get_attached_to, ":party_is_attached_to", ":party_no"),
					(lt, ":party_is_attached_to", 0),
					
					(store_troop_faction, ":faction_no", ":troop_no"),
					
					(try_begin),
						#(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
						(party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
						(party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
						(gt, ":commander_party", 0),
						(party_is_active, ":commander_party"),
						
						(assign, ":besieged_center", -1),
						(try_begin),
							(party_slot_eq, ":commander_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
							(party_get_slot, ":commander_object", ":commander_party", slot_party_ai_object), #get commander's ai object (center they are holding)
							(party_get_battle_opponent, ":besieger_enemy", ":commander_object"), #get this object's battle opponent
							(party_is_active, ":besieger_enemy"),
							(assign, ":besieged_center", ":commander_object"),
							(assign, ":commander_object", ":besieger_enemy"),
						(else_try),
							(party_slot_eq, ":commander_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
							(party_get_slot, ":commander_object", ":commander_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
							(ge, ":commander_object", 0), #if commander has an object
							(neg|is_between, ":commander_object", centers_begin, centers_end), #if this object is not a center, so it is a party
							(party_is_active, ":commander_object"),
							(party_get_battle_opponent, ":besieged_center", ":commander_object"), #get this object's battle opponent
						(else_try),
							(assign, ":besieged_center", -1),
						(try_end),
						
						(is_between, ":besieged_center", walled_centers_begin, walled_centers_end), #if battle opponent of our commander's ai object is a walled center
						
						(party_get_attached_to, ":attached_to_party", ":commander_party"), #if commander is attached to besieged center already.
						(eq, ":attached_to_party", ":besieged_center"),
						
						(store_faction_of_party, ":besieged_center_faction", ":besieged_center"),#get (battle opponent of our commander's ai object)'s faction
						(eq, ":besieged_center_faction", ":faction_no"), #if battle opponent of our commander's ai object is from same faction with current party
						(party_is_active, ":commander_object"),
						#make also follow_or_not check if needed
						
						(call_script, "script_party_set_ai_state", ":party_no", spai_engaging_army, ":commander_object"), #go and help commander
						
						(try_begin),
							(eq, "$cheat_mode", 1),
							(str_store_party_name, s7, ":party_no"),
							(str_store_party_name, s6, ":commander_object"),
							(display_message, "@{!}DEBUG : {s7} is helping his commander by fighting with {s6}."),
						(try_end),
					(else_try),
						#(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
						
						(party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
						(party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
						(gt, ":commander_party", 0),
						(party_is_active, ":commander_party"),
						
						(party_get_battle_opponent, ":besieged_center", ":commander_party"), #get this object's battle opponent
						
						#make also follow_or_not check if needed
						
						(is_between, ":besieged_center", walled_centers_begin, walled_centers_end), #if this object is a center
						(party_get_attached_to, ":attached_to_party", ":party_no"),
						(neq, ":attached_to_party", ":besieged_center"),
						(party_is_active, ":besieged_center"),
						
						(call_script, "script_party_set_ai_state", ":party_no", spai_engaging_army, ":besieged_center"), #go and help commander
						
						#(try_begin),
						#  (eq, "$cheat_mode", 1),
						#  (str_store_party_name, s7, ":party_no"),
						#  (str_store_party_name, s6, ":besieged_center"),
						#  (display_message, "@{!}DEBUG : {s7} is helping his commander by attacking {s6}."),
						#(try_end),
						
						#(party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
						#(party_set_ai_object, ":party_no", ":besieged_center"),
						#(party_set_flags, ":party_no", pf_default_behavior, 1), #is these needed?
						#(party_set_slot, ":party_no", slot_party_ai_substate, 1), #is these needed?
					(try_end),
				(try_end),
		])

# script_process_kingdom_parties_ai
		# This is called more frequently than decide_kingdom_parties_ai
		# WARNING: modified by 1257AD devs
		# Input: none
		# Output: none
		#called from triggers
process_kingdom_parties_ai = (
	"process_kingdom_parties_ai",
			[
			#tom
		# (assign, ":max_mod", 2), #tom was 3
		 
		# (assign, ":current_modula", "$g_alarm_modula"),
				# (val_add, "$g_hero_modula", 1),
				# (try_begin),
					# (eq, "$g_alarm_modula", ":max_mod"),
					# (assign, "$g_hero_modula", 0),
				# (try_end),
		#tom
				(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			# (store_mod, ":hero_modula", ":troop_no", ":max_mod"), #tom
					# (eq, ":hero_modula", ":current_modula"),				#tom
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
					(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
					(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
					(gt, ":party_no", 0),
					(call_script, "script_process_hero_ai", ":troop_no"),
				(try_end),
		])

		# script_process_hero_ai
		# This is called more frequently than script_decide_kingdom_party_ais
		# Handles sieges, raids, etc -- does not change the party's basic mission.
		# WARNING: modified by 1257AD devs
		# called from triggers
		# Input: none
		# Output: none
		
process_hero_ai = (
	"process_hero_ai",
			[
				(store_script_param_1, ":troop_no"),
				(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
				(try_begin),
					(party_is_active, ":party_no"),
					(store_faction_of_party, ":faction_no", ":party_no"),
					(party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
					(party_get_slot, ":ai_object", ":party_no", slot_party_ai_object),
					(try_begin),
						(eq, ":ai_state", spai_besieging_center),
						(try_begin),
							(party_slot_eq, ":ai_object", slot_center_is_besieged_by, -1),
							(store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
							(lt, ":distance", 3),
							(try_begin),
								(party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
								(party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
								(party_set_slot, ":ai_object", slot_center_is_besieged_by, ":commander_party"),
							(else_try),
								(party_set_slot, ":ai_object", slot_center_is_besieged_by, ":party_no"),
							(try_end),
							(store_current_hours, ":cur_hours"),
							(party_set_slot, ":ai_object", slot_center_siege_begin_hours, ":cur_hours"),
							
							(str_store_party_name_link, s1, ":ai_object"),
							(str_store_troop_name_link, s2, ":troop_no"),
							(str_store_faction_name_link, s3, ":faction_no"),
							# rafi
							(store_faction_of_party, ":ai_object_faction", ":ai_object"),
							#(store_troop_faction, ":troop_faction", ":troop_no"),
							# update AI for target
							(assign, ":saved_glob", "$g_ai_kingdom"),
							(assign, "$g_ai_kingdom", ":ai_object_faction"),
							(call_script, "script_recalculate_ais"),
							(assign, "$g_ai_kingdom", ":saved_glob"),
							# end AI update
							# (store_relation, ":rel", ":troop_faction", "$players_kingdom"),
							# (try_begin),
								# (this_or_next | lt, ":rel", 0),
								# (this_or_next | eq, ":ai_object_faction", "$players_kingdom"),
								# (eq, ":troop_faction", "$players_kingdom"),
								# (str_store_faction_name_link, s3, ":troop_faction"),
								# (display_log_message, "@{s1} has been besieged by {s2} of {s3}."),
							# (try_end),
							# end rafi
							
							(try_begin),
								(store_faction_of_party, ":ai_object_faction", ":ai_object"),
								(this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
								(eq, ":ai_object_faction", "fac_player_supporters_faction"),
								(call_script, "script_add_notification_menu", "mnu_notification_center_under_siege", ":ai_object", ":troop_no"),
							(try_end),
							(call_script, "script_village_set_state", ":ai_object", svs_under_siege),
							
							(store_faction_of_party, ":ai_object_faction", ":ai_object"),
							# (call_script, "script_raf_set_ai_recalculation_flags", ":faction_no"),
							# (call_script, "script_raf_set_ai_recalculation_flags", ":ai_object_faction"),
							(assign, "$g_recalculate_ais", 1),
						(try_end),
					(else_try),
						(eq, ":ai_state", spai_raiding_around_center),
						(party_slot_eq, ":party_no", slot_party_ai_substate, 0),
						(assign, ":selected_village", 0),
						(try_for_range, ":enemy_village_no", villages_begin, villages_end),
							(eq, ":selected_village", 0),
							(store_faction_of_party, ":enemy_village_faction", ":enemy_village_no"),
							(try_begin),
								(party_slot_eq, ":enemy_village_no", slot_town_lord, "trp_player"),
								(store_relation, ":reln", "fac_player_supporters_faction", ":faction_no"),
							(else_try),
								(store_relation, ":reln", ":enemy_village_faction", ":faction_no"),
							(try_end),
							(lt, ":reln", 0),
							(store_distance_to_party_from_party, ":dist", ":enemy_village_no", ":party_no"),
							(lt, ":dist", 15),
							(party_slot_eq, ":enemy_village_no", slot_village_state, 0), #village is not already raided
							#CHANGE STATE TO RAID THIS VILLAGE
							(assign, ":selected_village", ":enemy_village_no"),
						(try_end),
						(try_begin),
							(eq, ":selected_village", 0),
							(is_between, ":ai_object", villages_begin, villages_end),
							(assign, ":selected_village", ":ai_object"),
						(try_end),
						(try_begin),
							(gt, ":selected_village", 0),
							(call_script, "script_party_set_ai_state", ":party_no", spai_raiding_around_center, ":selected_village"),
							(try_begin),
								(faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
								(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
								(faction_set_slot, ":faction_no", slot_faction_ai_object, ":selected_village"),
							(try_end),
							(party_get_position, pos1, ":selected_village"),
							(map_get_random_position_around_position, pos2, pos1, 1),
							(party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
							(party_set_ai_target_position, ":party_no", pos2),
							(party_set_ai_object, ":party_no", ":selected_village"),
							(party_set_slot, ":party_no", slot_party_ai_substate, 1),
						(try_end),
					(else_try),
						(eq, ":ai_state", spai_raiding_around_center),#substate is 1
						(try_begin),
							(store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
							(lt, ":distance", 2),
							(try_begin),
								(party_slot_eq, ":ai_object", slot_village_state, 0),
								(call_script, "script_village_set_state", ":ai_object", svs_being_raided),
								(party_set_slot, ":ai_object", slot_village_raided_by, ":party_no"),
								(try_begin),
									(store_faction_of_party, ":village_faction", ":ai_object"),
									(this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
									(eq, ":village_faction", "fac_player_supporters_faction"),
									(store_distance_to_party_from_party, ":dist", "p_main_party", ":ai_object"),
									(this_or_next|lt, ":dist", 30),
									(party_slot_eq, ":ai_object", slot_center_has_messenger_post, 1),
									(call_script, "script_add_notification_menu", "mnu_notification_village_raid_started", ":ai_object", ":troop_no"),
								(try_end),
							(else_try),
								(party_slot_eq, ":ai_object", slot_village_state, svs_being_raided),
							(else_try),
								#if anything other than being_raided leave
								(party_set_slot, ":party_no", slot_party_ai_substate, 0),
							(try_end),
						(try_end),
					(else_try),
						(eq, ":ai_state", spai_retreating_to_center),
						(try_begin),
							(party_get_battle_opponent, ":enemy_party", ":party_no"),
							(ge, ":enemy_party", 0), #we are in a battle! we may be caught in a loop!
							(call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
							(party_set_flags, ":party_no", pf_default_behavior, 0),
							(party_set_slot, ":party_no", slot_party_commander_party, -1),
						(try_end),
					(else_try),
						(eq, ":ai_state", spai_patrolling_around_center),
						
						(try_begin),
							(party_slot_eq, ":party_no", slot_party_ai_substate, 0),
							(store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
							(lt, ":distance", 6),
							(party_set_slot, ":party_no", slot_party_ai_substate, 1),
							
							(party_set_aggressiveness, ":party_no", 8),
							(party_set_courage, ":party_no", 8),
							(party_set_ai_initiative, ":party_no", 100),
							
							(party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
							(party_set_ai_object, ":party_no", ":ai_object"),
						(try_end),
					(else_try),
						(eq, ":ai_state", spai_holding_center),
					(try_end),
				(try_end),
		])


		# script_begin_assault_on_center
		# called from triggers
		# Input: arg1: faction_no
		# Output: none
begin_assault_on_center = (
	"begin_assault_on_center",
			[
				(store_script_param, ":center_no", 1),
				
				(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
					(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
					(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
					(gt, ":party_no", 0),
					(party_is_active, ":party_no"),
					
					(assign, ":continue", 0),
					(try_begin),
						(party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
						(party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
						(party_slot_eq, ":party_no", slot_party_ai_substate, 0),
						(assign, ":continue", 1),
					(else_try),
						(party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
						(party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
						(gt, ":commander_party", 0),
						(party_is_active, ":commander_party"),
						(party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
						(party_slot_eq, ":commander_party", slot_party_ai_object, ":center_no"),
						(call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
						(assign, ":continue", 1),
					(try_end),
					
					(eq, ":continue", 1),
					
					(party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
					(party_set_ai_object, ":party_no", ":center_no"),
					(party_set_flags, ":party_no", pf_default_behavior, 1),
					(party_set_slot, ":party_no", slot_party_ai_substate, 1),
				(try_end),
		])


    # script_lift_siege
    # Input: arg1 = center_no, arg2 = display_message
    # Output: none
    #called from triggers
lift_siege = (
	"lift_siege",
	[
		(store_script_param, ":center_no", 1),
		(store_script_param, ":display_message", 2),
		(party_set_slot, ":center_no", slot_center_is_besieged_by, -1), #clear siege
		(call_script, "script_village_set_state",  ":center_no", 0), #clear siege flag
		(try_begin),
			(eq, ":center_no", "$g_player_besiege_town"),
			(assign, "$g_siege_method", 0), #remove siege progress
		(try_end),
		(try_begin),
         	(eq, ":display_message", 1),
         	(str_store_party_name_link, s3, ":center_no"),
         	(display_message, "@{s3} is no longer under siege."),
        (try_end),
    ])

# script_decide_faction_ai
		# called from triggers
		# WARNING : heavily modified by 1257AD devs
		# note : "abc begins an offensive.  Curret target is xyz" messages are also printed from this procedure
		# Input: arg1: faction_no
		# Output: none
decide_faction_ai = (
	"decide_faction_ai",
			#This handles political issues and faction issues
			[
				(store_script_param_1, ":faction_no"),
				
				
				(faction_get_slot, ":old_faction_ai_state", ":faction_no", slot_faction_ai_state),
				(faction_get_slot, ":old_faction_ai_object", ":faction_no", slot_faction_ai_object),
				(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
				
				
				#Remove marshal if he has become too controversial,, or he has defected, or has been taken prisoner
				(try_begin),
					(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
					(neq, ":faction_no", "fac_player_supporters_faction"),
					(ge, ":faction_marshal", "trp_player"),
					
					(store_faction_of_troop, ":marshal_faction", ":faction_marshal"),
					(try_begin),
						(eq, ":faction_marshal", "trp_player"),
						(assign, ":marshal_faction", "$players_kingdom"),
					(try_end),
					
					
					(assign, ":player_marshal_is_prisoner", 0),
					(try_begin),
						(eq, ":faction_marshal", "trp_player"),
						(eq, "$g_player_is_captive", 1),
						(assign, ":player_marshal_is_prisoner", 1),
					(try_end),
					
					
					#High controversy level, or marshal has defected, or is prisoner
					(this_or_next|neq, ":marshal_faction", ":faction_no"),
					(this_or_next|troop_slot_ge, ":faction_marshal", slot_troop_controversy, 80),
					(this_or_next|eq, ":player_marshal_is_prisoner", 1),
					(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
					
					(assign, ":few_following_player_campaign", 0),
					(try_begin),
						(eq, ":faction_marshal", "trp_player"),
						(assign, ":vassals_following_player_campaign", 0),
						(gt, "$g_player_days_as_marshal", 1),
						(try_for_range, ":vassal", active_npcs_begin, active_npcs_end),
							(troop_slot_eq, ":vassal", slot_troop_occupation, slto_kingdom_hero),
							(store_faction_of_troop, ":vassal_faction", ":vassal"),
							(eq, ":vassal_faction", ":faction_no"),
							(call_script, "script_npc_decision_checklist_troop_follow_or_not", ":vassal"),
							(eq, reg0, 1),
							(val_add, ":vassals_following_player_campaign", 1),
						(try_end),
						(lt, ":vassals_following_player_campaign", 4),
						(assign, ":few_following_player_campaign", 1),
					(try_end),
					
					#Only remove marshal for controversy if offensive campaign in progress
					(this_or_next|eq, ":old_faction_ai_state", sfai_default),
					(this_or_next|eq, ":old_faction_ai_state", sfai_feast),
					(this_or_next|neq, ":marshal_faction", ":faction_no"),
					(this_or_next|eq, ":few_following_player_campaign", 1),
					(this_or_next|eq, ":player_marshal_is_prisoner", 1),
					(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
					
					#No current issue on the agenda
					(this_or_next|faction_slot_eq, ":faction_no", slot_faction_political_issue, 0),
					(this_or_next|eq, ":player_marshal_is_prisoner", 1),
					(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
					
					(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
					(store_current_hours, ":hours"),
					(val_max, ":hours", 0),
					(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
					
					(faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),
					(try_begin),
						(ge, ":old_marshall", 0),
						(troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
						(party_is_active, ":old_marshall_party"),
						(party_set_marshall, ":old_marshall_party", 0),
					(try_end),
					
					(try_begin),
						(eq, "$players_kingdom", ":faction_no"),
						(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
						(call_script, "script_add_notification_menu", "mnu_notification_relieved_as_marshal", 0, 0),
					(else_try),
						(neq, ":old_marshall", "trp_player"),
						(call_script, "script_change_troop_renown", ":old_marshall", 15),
					(try_end),
					(faction_set_slot, ":faction_no", slot_faction_marshall, -1),
					(assign, ":faction_marshal", -1),
					
					
					
					(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
						(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
						(eq, ":active_npc_faction", ":faction_no"),
						(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					(try_begin),
						(eq, "$players_kingdom", ":faction_no"),
						(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					
				(else_try),	 #If marshal not present, and not already on agenda, make political issue
					(eq, ":faction_marshal", -1),
					(neg|faction_slot_ge, ":faction_no", slot_faction_political_issue, 1), #This to avoid resetting votes every time
					
					(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
					(neq, ":faction_no", "fac_player_supporters_faction"),
					
					(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
					(store_current_hours, ":hours"),
					(val_max, ":hours", 0),
					(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
					
					(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
						(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
						(eq, ":active_npc_faction", ":faction_no"),
						(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					(try_begin),
						(eq, "$players_kingdom", ":faction_no"),
						(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					
					
				(else_try),	#If player is marshal, but not part of faction
					(eq, ":faction_marshal", "trp_player"),
					(neq, "$players_kingdom", ":faction_no"),
					
					(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
					(store_current_hours, ":hours"),
					(val_max, ":hours", 0),
					(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
					
					(faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),
					(try_begin),
						(ge, ":old_marshall", 0),
						(troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
						(party_is_active, ":old_marshall_party"),
						(party_set_marshall, ":old_marshall_party", 0),
					(try_end),
					
					(faction_set_slot, ":faction_no", slot_faction_marshall, -1),
					(assign, ":faction_marshal", -1),
					
					(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
						(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
						(eq, ":active_npc_faction", ":faction_no"),
						(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					(try_begin),
						(eq, "$players_kingdom", ":faction_no"),
						(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					
				(try_end),
				
				#If the faction issue is a center no longer under faction control, remove and reset
				(try_begin),
					(faction_get_slot, ":faction_political_issue", ":faction_no", slot_faction_political_issue),
					(is_between, ":faction_political_issue", centers_begin, centers_end),
					(store_faction_of_party, ":disputed_center_faction", ":faction_political_issue"),
					(neq, ":disputed_center_faction", ":faction_no"),
					
					(try_begin),
						(eq, "$cheat_mode", 1),
						(str_store_faction_name, s4, ":faction_no"),
						(str_store_party_name, s5, ":disputed_center_faction"),
						(display_message, "@{!}DEBUG -- {s4} drops {s5} as issue as it has changed hands"),
					(try_end),
					
					#Reset political issue
					(faction_set_slot, ":faction_no", slot_faction_political_issue, 0),
					(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
						(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
						(eq, ":active_npc_faction", ":faction_no"),
						(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					(try_begin),
						(eq, "$players_kingdom", ":faction_no"),
						(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					
				(try_end),
				
				
				#Resolve the political issue on the agenda
				(try_begin),
					(faction_slot_ge, ":faction_no", slot_faction_political_issue, 1),
					(neq, ":faction_no", "fac_player_supporters_faction"),
					
					#Do not switch marshals during a campaign
					(this_or_next|faction_slot_ge, ":faction_no", slot_faction_political_issue, centers_begin),
					(this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_default),
					(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
					
					
					(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
					
					(assign, ":total_lords", 0),
					(assign, ":lords_who_have_voted", 0),
					(assign, ":popular_favorite", -1),
					
					#Reset number of votes
					(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
					(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
						(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
					(try_end),
					
					#Tabulate votes
					(try_for_range, ":voting_lord", active_npcs_begin, active_npcs_end),
						(store_faction_of_troop, ":voting_lord_faction", ":voting_lord"),
						(eq, ":voting_lord_faction", ":faction_no"),
						(val_add, ":total_lords", 1),
						(troop_get_slot, ":lord_chosen_candidate", ":voting_lord", slot_troop_stance_on_faction_issue),
						(gt, ":lord_chosen_candidate", -1),
						(val_add, ":lords_who_have_voted", 1),
						(troop_get_slot, ":total_votes", ":lord_chosen_candidate", slot_troop_temp_slot),
						(val_add, ":total_votes", 1),
						(troop_set_slot, ":lord_chosen_candidate", slot_troop_temp_slot, ":total_votes"),
						(try_begin),
							(gt, ":popular_favorite", -1),
							(troop_get_slot, ":current_winner_votes", ":popular_favorite", slot_troop_temp_slot),
							(gt, ":total_votes", ":current_winner_votes"),
							(assign, ":popular_favorite", ":lord_chosen_candidate"),
						(else_try),
							(eq, ":popular_favorite", -1),
							(assign, ":popular_favorite", ":lord_chosen_candidate"),
						(try_end),
					(try_end),
					
					#Check to see if enough lords have voted
					(store_div, ":number_required_for_quorum", ":total_lords", 5),
					(val_mul, ":number_required_for_quorum", 4),
					
					
					#		(gt, ":lords_who_have_voted", ":number_required_for_quorum"),
					
					(store_current_hours, ":hours_on_agenda"),
					(faction_get_slot, ":hours_when_put_on_agenda", ":faction_no", slot_faction_political_issue_time), #Appointment of marshal
					(val_sub, ":hours_on_agenda", ":hours_when_put_on_agenda"),
					
					(this_or_next|gt, ":lords_who_have_voted", ":number_required_for_quorum"),
					(ge, ":hours_on_agenda", 120),
					
					(try_begin),
						(eq, "$cheat_mode", 1),
						(assign, reg4, ":lords_who_have_voted"),
						(assign, reg5, ":number_required_for_quorum"),
						(assign, reg7, ":hours_on_agenda"),
						(str_store_faction_name, s4, ":faction_no"),
						(display_message, "@{!}DEBUG -- Issue resolution for {s4}: {reg4} votes for a quorum of {reg5}, {reg7} hours on agenda"),
					(try_end),
					
					
					(try_begin),
						(eq, "$cheat_mode", 1),
						(display_message, "@{!}DEBUG -- Faction resolves political issue"),
					(try_end),
					
					
					#Resolve faction political issue
					(assign, ":winning_candidate", -1),
					(try_begin),
						(call_script, "script_troop_get_relation_with_troop", ":faction_leader", ":popular_favorite"),
						
						(this_or_next|ge, reg0, 10),
						(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_stance_on_faction_issue, ":popular_favorite"),
						(troop_slot_eq, ":faction_leader", slot_troop_stance_on_faction_issue, -1),
						
						(assign, ":winning_candidate", ":popular_favorite"),
					(else_try),#Lord overrules lords' opinion
						(gt, ":faction_leader", -1), #not sure why this is necessary
						(troop_get_slot, ":liege_choice", ":faction_leader", slot_troop_stance_on_faction_issue),
						(ge, ":liege_choice", -1),
						
						(assign, ":winning_candidate", ":liege_choice"),
					(try_end),
					
					#Carry out faction decision
					(try_begin), #Nothing happens
						(eq, ":winning_candidate", -1),
						
					(else_try), #For player, create a menu to accept or refuse
						(eq, ":winning_candidate", "trp_player"),
						(eq, "$players_kingdom", ":faction_no"),
						(call_script, "script_add_notification_menu", "mnu_notification_player_faction_political_issue_resolved_for_player", 0, 0),
					(else_try),
						(eq, ":winning_candidate", "trp_player"),
						(neq, "$players_kingdom", ":faction_no"),
						
						(try_begin),
							(eq, "$cheat_mode", 1),
							(str_store_faction_name, s4, ":faction_no"),
							(str_store_party_name, s5, ":winning_candidate"),
							(display_message, "@{!}DEBUG -- {s4} drops {s5} as winner, for having changed sides"),
						(try_end),
						
						(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
							(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
							(eq, ":active_npc_faction", ":faction_no"),
							(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
						(try_end),
						(try_begin),
							(eq, "$players_kingdom", ":faction_no"),
							(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
						(try_end),
						
					(else_try),	#If candidate is not of winning faction, reset lrod votes
						(store_faction_of_troop, ":winning_candidate_faction", ":winning_candidate"),
						(neq, ":winning_candidate_faction", ":faction_no"),
						
						(try_begin),
							(eq, "$cheat_mode", 1),
							(str_store_faction_name, s4, ":faction_no"),
							(str_store_party_name, s5, ":winning_candidate"),
							(display_message, "@{!}DEBUG -- {s4} drops {s5} as winner, for having changed sides"),
						(try_end),
						
						(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
							(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
							(eq, ":active_npc_faction", ":faction_no"),
							(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
						(try_end),
						(try_begin),
							(eq, "$players_kingdom", ":faction_no"),
							(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
						(try_end),
						
					(else_try), #Honor awarded to another
						(faction_get_slot, ":issue_on_table", ":faction_no", slot_faction_political_issue),
						(try_begin), #A marshalship awarded to another
							(eq, ":issue_on_table", 1),
							(is_between, ":winning_candidate", active_npcs_begin, active_npcs_end),
							
							(this_or_next|is_between, ":winning_candidate", active_npcs_begin, active_npcs_end), #Prevents bug in which player given marshaldom of kingdom of which he/she is not a member
							(eq, "$players_kingdom", ":faction_no"),
							
							(assign, ":faction_marshal", ":winning_candidate"),
						(else_try), #A fief awarded to another
							(is_between, ":issue_on_table", centers_begin, centers_end),
							
							#If given to the player, resolved above
							(call_script, "script_give_center_to_lord", ":issue_on_table", ":winning_candidate", 0), #Zero means don't add garrison
							
							#If the player had requested a captured castle
							(try_begin),
								(eq, ":issue_on_table", "$g_castle_requested_by_player"),
								(party_slot_ge, ":issue_on_table", slot_town_lord, active_npcs_begin),
								(store_faction_of_party, ":faction_of_issue", ":issue_on_table"),
								(eq, ":faction_of_issue", "$players_kingdom"),
								(assign, "$g_center_to_give_to_player", ":issue_on_table"),
								(try_begin),
									(troop_get_slot, ":husband", "trp_player", slot_troop_spouse),
									(is_between, ":husband", active_npcs_begin, active_npcs_end),
									(eq, "$g_castle_requested_for_troop", ":husband"),
									(neq, ":winning_candidate", ":husband"),
									(jump_to_menu, "mnu_requested_castle_granted_to_another_female"),
								(else_try),
									(jump_to_menu, "mnu_requested_castle_granted_to_another"),
								(try_end),
							(try_end),
							
						(try_end),
						
						(try_begin),
							(eq, ":faction_no", "$players_kingdom"),
							(call_script, "script_add_notification_menu", "mnu_notification_player_faction_political_issue_resolved", ":issue_on_table", ":winning_candidate"),
						(try_end),
						
						#Reset political issue
						(faction_set_slot, ":faction_no", slot_faction_political_issue, 0),
						(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
							(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
							(eq, ":active_npc_faction", ":faction_no"),
							(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
						(try_end),
						(try_begin),
							(eq, "$players_kingdom", ":faction_no"),
							(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
						(try_end),
					(try_end),
				(try_end),
				
				#Add fief to faction issues
				(try_begin),
					(faction_get_slot, ":faction_issue", ":faction_no", slot_faction_political_issue),
					(le, ":faction_issue", 0),
					
					(assign, ":landless_lords", 0),
					(assign, ":unassigned_centers", 0),
					(assign, ":first_unassigned_center_found", 0),
					
					(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
					(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
						(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
					(try_end),
					
					(try_for_range, ":center", centers_begin, centers_end),
						(store_faction_of_party, ":center_faction", ":center"),
						(eq, ":center_faction", ":faction_no"),
						
						(party_get_slot, ":town_lord", ":center", slot_town_lord),
						
						(try_begin),
							(lt, ":town_lord", 0),
							(val_add, ":unassigned_centers", 1),
							(try_begin),
								(eq, ":first_unassigned_center_found", 0),
								(assign, ":first_unassigned_center_found", ":center"),
							(try_end),
						(else_try),
							(troop_set_slot, ":town_lord", slot_troop_temp_slot, 1),
						(try_end),
					(try_end),
					
					(store_add, ":landless_lords_plus_unassigned_centers", ":landless_lords", ":unassigned_centers"),
					(ge, ":landless_lords_plus_unassigned_centers", 2),
					
					(faction_set_slot, ":faction_no", slot_faction_political_issue, ":first_unassigned_center_found"),
					(store_current_hours, ":hours"),
					(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Fief put on agenda
					
					(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
						(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
						(eq, ":active_npc_faction", ":faction_no"),
						(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
					(try_end),
					(try_begin),
						(eq, "$players_kingdom", ":faction_no"),
						(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
					(try_end),
				(try_end),
				
				
				(try_begin), #If the marshal is changed
					(neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshal"),
					#(assign, ":marshall_changed", 1),
					(eq, "$players_kingdom", ":faction_no"),
					(str_store_troop_name_link, s1, ":faction_marshal"),
					(str_store_faction_name_link, s2, ":faction_no"),
					(display_message, "@{s1} is the new marshal of {s2}."),
					(call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),
				(try_end),
				
				(try_begin), #If the marshal is changed
					(neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshal"),
					(gt, ":faction_marshal", -1),
					(call_script, "script_appoint_faction_marshall", ":faction_no", ":faction_marshal"),
				(try_end),
				
				#DO FACTION AI HERE
				(try_begin),
					(eq, ":faction_no", "$players_kingdom"),
					(eq, ":faction_marshal", "trp_player"),
					(assign, ":faction_ai_decider", "trp_player"),
				(else_try),
					(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
					(assign, ":faction_ai_decider", ":faction_marshal"),
				(else_try),
					(faction_get_slot, ":faction_ai_decider", ":faction_no", slot_faction_leader),
				(try_end),
				
				(call_script, "script_npc_decision_checklist_faction_ai_alt",  ":faction_ai_decider"),
				(assign, ":new_strategy", reg0),
				(assign, ":new_object", reg1),
				
				#new ozan
				(try_begin),
					(neq, ":new_strategy", ":old_faction_ai_state"),
					(eq, ":new_strategy", sfai_gathering_army),
					(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
					(troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
					(party_set_slot, ":marshal_party", slot_party_ai_object, -1),
					(assign, "$g_gathering_new_started", 1),
					(call_script, "script_npc_decision_checklist_party_ai", ":faction_marshal"), #This handles AI for both marshal and other parties
					(call_script, "script_party_set_ai_state", ":marshal_party", reg0, reg1),
					(assign, "$g_gathering_new_started", 0),
					#rafi
					(try_begin),
						(eq, ":faction_no", "$players_kingdom"),
						(str_store_faction_name, s21, ":faction_no"),
						(str_store_troop_name, s22, ":faction_marshal"),
						(str_store_party_name, s23, reg1),
						(display_message, "@{s22}, the marshal of {s21}, decides to gather the army around {s23}.", 0xff5e8bff),
					(try_end),
					#end rafi
				(else_try),
					#check if marshal arrived his target city during active gathering
					
					#for now i disabled below lines because after always/active gathering armies become very large.
					#in current style marshal makes active gathering only at first, it travels to a city and waits there.
					
					(eq, ":new_strategy", ":old_faction_ai_state"),
					(eq, ":new_strategy", sfai_gathering_army),
					(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
					(troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
					(party_get_slot, ":party_ai_object", ":marshal_party", slot_party_ai_object),
					(ge, ":party_ai_object", 0),
					(store_distance_to_party_from_party, ":dist", ":marshal_party", ":party_ai_object"),
					(le, ":dist", 5),
					(party_set_slot, ":marshal_party", slot_party_ai_object, -1),
				(try_end),
				#end ozan
				
				#The following logic is mostly transplanted to the new decision_checklist
				#Decision_checklist is used because I want to be able to reproduce the logic for strings
				#(call_script, "script_old_faction_ai"),
				#ozan - I collected all comment-out lines in here (faction ai script) and placed most bottom of scripts.py to avoid confusing.
				
				(faction_set_slot, ":faction_no", slot_faction_ai_state, ":new_strategy"),
				(faction_set_slot, ":faction_no", slot_faction_ai_object, ":new_object"),
				
				(call_script, "script_update_report_to_army_quest_note", ":faction_no", ":new_strategy", ":old_faction_ai_state"),
				
				(try_begin),
					(eq, ":new_strategy", sfai_feast),
					
					(store_current_hours, ":hours"),
					(faction_set_slot, ":faction_no", slot_faction_last_feast_start_time, ":hours"), #new
					
					(try_begin),
						(eq, "$g_player_eligible_feast_center_no", ":new_object"),
						(assign, "$g_player_eligible_feast_center_no", -1), #reset needed
					(try_end),
					(try_begin),
						(is_between, ":new_object", towns_begin, towns_end),
						(party_set_slot, ":new_object", slot_town_has_tournament, 2),
					(try_end),
				(try_end),
				
				#Change of strategy
				(try_begin),
					(neq, ":new_strategy", ":old_faction_ai_state"),
					
					(try_begin),
						(ge, "$cheat_mode", 1),
						(str_store_faction_name, s5, ":faction_no"),
						(display_message, "str_s5_decides_s14"),
					(try_end),
					
					(store_current_hours, ":hours"),
					(faction_set_slot, ":faction_no", slot_faction_ai_current_state_started, ":hours"),
					
					#Feast ends
					(try_begin),
						(eq, ":old_faction_ai_state", sfai_feast),
						(call_script, "script_faction_conclude_feast", ":faction_no", ":old_faction_ai_object"),
					(try_end),
					
					
					#Feast begins
					(try_begin),
						(eq, ":new_strategy", sfai_feast),
						(faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
						
						##         (str_store_faction_name, s1, ":faction_no"),
						##         (str_store_party_name, s2, ":faction_object"),
						##         (display_message, "str_lords_of_the_s1_gather_for_a_feast_at_s2"),
						
						(party_get_slot, ":feast_host", ":faction_object", slot_town_lord),
						
						(try_begin),
							(check_quest_active, "qst_wed_betrothed"),
							
							(quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, ":feast_host"),
							(neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
							(call_script, "script_add_notification_menu", "mnu_notification_player_wedding_day", ":feast_host", ":faction_object"),
						(else_try),
							(check_quest_active, "qst_wed_betrothed_female"),
							
							(quest_get_slot, ":player_betrothed", "qst_wed_betrothed", slot_quest_giver_troop),
							(store_faction_of_troop, ":player_betrothed_faction", ":player_betrothed"),
							(eq, ":player_betrothed_faction", ":faction_no"),
							(neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
							(call_script, "script_add_notification_menu", "mnu_notification_player_kingdom_holds_feast", ":feast_host", ":faction_object"),
						(else_try),
							(eq, "$players_kingdom", ":faction_no"),
							(troop_slot_ge, "trp_player", slot_troop_renown, 150),
							
							
							(party_get_slot, ":feast_host", ":faction_object", slot_town_lord),
							(call_script, "script_add_notification_menu", "mnu_notification_player_kingdom_holds_feast", ":feast_host", ":faction_object"),
						(try_end),
					(try_end),
					
					
					#Offensive begins
					(try_begin),
						(eq, ":old_faction_ai_state", sfai_gathering_army),
						(is_between, ":new_strategy", sfai_attacking_center, sfai_feast),
						(try_begin),
							#(eq, "$cheat_mode", 1),
							(str_store_faction_name, s5, ":faction_no"),
							(faction_get_slot, ":target", ":faction_no", slot_faction_ai_object),
							(gt, ":target", 0),
							(str_store_party_name, s22, ":target"),
							(this_or_next | eq, ":faction_no", "fac_player_supporters_faction"),
							(eq, ":faction_no", "$players_kingdom"),
							#(display_message, "str_s5_begins_offensive"),
							(display_message, "@{s5} begins an offensive.  Curret target is {s22}", info_clr),
						(try_end),
						
						#Appoint screening party
						(try_begin),
							(assign, ":total_lords_participating", 0),
							(assign, ":best_screening_party", -1),
							(assign, ":score_to_beat", 30), #closest in size to 50
							(troop_get_slot, ":faction_marshal_party", ":faction_marshal", slot_troop_leaded_party),
							(party_is_active, ":faction_marshal_party"),
							
							(try_for_range, ":screen_leader", active_npcs_begin, active_npcs_end),
								(store_faction_of_troop, ":screen_leader_faction", ":screen_leader"),
								(eq, ":screen_leader_faction", ":faction_no"),
								
								(troop_get_slot, ":screening_party", ":screen_leader", slot_troop_leaded_party),
								(party_is_active, ":screening_party"),
								(party_slot_eq, ":screening_party", slot_party_ai_state, spai_accompanying_army),
								(party_slot_eq, ":screening_party", slot_party_ai_object, ":faction_marshal_party"),
								(val_add, ":total_lords_participating", 1),
								
								(try_begin),
									(ge, "$cheat_mode", 1),
									(str_store_party_name, s4, ":screening_party"),
									(display_message, "@{!}DEBUG -- {s4} participates in offensive"),
								(try_end),
								
								
								(store_party_size_wo_prisoners, ":screening_party_score", ":screening_party"),
								(val_sub, ":screening_party_score", 50),
								(val_abs, ":screening_party_score"),
								
								
								(lt, ":screening_party_score", ":score_to_beat"),
								
								#set party and score
								(assign, ":best_screening_party", ":screening_party"),
								(assign, ":score_to_beat", ":screening_party_score"),
							(try_end),
							
							(gt, ":total_lords_participating", 2),
							(party_is_active, ":best_screening_party"),
							(party_is_active, ":faction_marshal_party"),
							(call_script, "script_party_set_ai_state", ":best_screening_party", spai_screening_army, ":faction_marshal_party"),
							(try_begin),
								(ge, "$cheat_mode", 1),
								(str_store_party_name, s4, ":best_screening_party"),
								(display_message, "@{!}DEBUG -- {s4} chosen as screen"),
							(try_end),
							#after this - dialogs on what doing, npc_decision_checklist
						(try_end),
						
						#Offensive concludes
					(else_try),
						(store_current_hours, ":hours"),
						(this_or_next|eq, ":old_faction_ai_state", sfai_gathering_army),
						(this_or_next|eq, ":old_faction_ai_state", sfai_attacking_center),
						(this_or_next|eq, ":old_faction_ai_state", sfai_raiding_village),
						#(this_or_next|eq, ":old_faction_ai_state", sfai_attacking_enemies_around_center),
						(eq, ":old_faction_ai_state", sfai_attacking_enemy_army),
						
						(this_or_next|eq, ":new_strategy", sfai_default),
						(eq, ":new_strategy", sfai_feast),
						
						(call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),
						(faction_set_slot, ":faction_no", slot_faction_last_offensive_concluded, ":hours"),
					(try_end),
				(try_end),
				
				(try_begin),
					(eq, "$players_kingdom", ":faction_no"),
					(neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
					(check_quest_active, "qst_join_siege_with_army"),
					(call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
				(try_end),
				
				(try_begin),
					#old condition to rest, I changed below part - ozan, to rest (a faction's old strategy should be feast or default) and (a faction's new strategy should be feast or default)
					#(this_or_next|eq, ":new_strategy", sfai_default),
					#(this_or_next|eq, ":new_strategy", sfai_feast),
					#(this_or_next|eq, ":old_faction_ai_state", sfai_default),
					#(eq, ":old_faction_ai_state", sfai_feast),
					
					#new condition to rest, (a faction's new strategy should be feast or default) and (":hours_at_current_state" > 20)
					(this_or_next|eq, ":new_strategy", sfai_default),
					(eq, ":new_strategy", sfai_feast),
					
					(store_current_hours, ":hours_at_current_state"),
					(faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started),
					(val_sub, ":hours_at_current_state", ":current_state_started"),
					(ge, ":hours_at_current_state", 18), #Must have at least 18 hours to reset
					
					(store_current_hours, ":hours"),
					(faction_set_slot, ":faction_no", slot_faction_ai_last_rest_time, ":hours"),
				(try_end),
		])

# script_encounter_calculate_fit
		# Input: arg1 = troop_no
		# Output: none
encounter_calculate_fit = (
	"encounter_calculate_fit",
			[
				#(assign, "$g_enemy_fit_for_battle_old",  "$g_enemy_fit_for_battle"),
				#(assign, "$g_friend_fit_for_battle_old", "$g_friend_fit_for_battle"),
				#(assign, "$g_main_party_fit_for_battle_old", "$g_main_party_fit_for_battle"),
				(call_script, "script_party_count_fit_for_battle", "p_main_party"),
				#(assign, "$g_main_party_fit_for_battle", reg(0)),
				(call_script, "script_collect_friendly_parties"),
				(call_script, "script_party_count_fit_for_battle", "p_collective_friends"),
				(assign, "$g_friend_fit_for_battle", reg(0)),
				
				(party_clear, "p_collective_ally"),
				(try_begin),
					(gt, "$g_ally_party", 0),
					(party_is_active, "$g_ally_party"),
					(party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),
					#(call_script, "script_party_count_fit_for_battle", "p_collective_ally"),
					#(val_add, "$g_friend_fit_for_battle", reg(0)),
				(try_end),
				
				(party_clear, "p_collective_enemy"),
				(try_begin),
					(party_is_active, "$g_enemy_party"),
					(party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),
				(try_end),
				(call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
				(assign, "$g_enemy_fit_for_battle", reg(0)),
				(assign, reg11, "$g_enemy_fit_for_battle"),
				(assign, reg10, "$g_friend_fit_for_battle"),
		])
		
		# script_encounter_init_variables
		# part of freelancer script is in this procedure
		# WARNING : HEAVILY modified by 1257AD devs
		# Input: arg1 = troop_no
		# Output: none
encounter_init_variables = (
	"encounter_init_variables",
			[
				(assign, "$capture_screen_shown", 0),
				(assign, "$loot_screen_shown", 0),
				(assign, "$thanked_by_ally_leader", 0),
				(assign, "$g_battle_result", 0),
				(assign, "$cant_leave_encounter", 0),
				(assign, "$cant_talk_to_enemy", 0),
				(assign, "$last_defeated_hero", 0),
				(assign, "$last_freed_hero", 0),
				
				(call_script, "script_encounter_calculate_fit"),
				(call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
				(call_script, "script_party_calculate_strength", "p_main_party", 0),
				(assign, "$g_starting_strength_main_party", reg0),
				(call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
				(call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
				(assign, "$g_starting_strength_enemy_party", reg0),
				(assign, "$g_strength_contribution_of_player", 100),
				
				(call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
				(call_script, "script_party_calculate_strength", "p_collective_friends", 0),
				(assign, "$g_starting_strength_friends", reg0),
				
				(store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 100), # reduce contribution if we are helping someone.
				
				(try_begin),
		#Caba freelancer fixes chief
			(eq, "$freelancer_state", 1),
			(store_character_level, "$g_strength_contribution_of_player", "$player_cur_troop"),
			(val_div, "$g_strength_contribution_of_player", 2),
			(val_max, "$g_strength_contribution_of_player", 5), #contribution(scale 0-100) = level/2, min 5 (so about 5-25)
			#(store_character_level, ":freelancer_player_contribution", "$player_cur_troop"),
			#(val_mul, ":freelancer_player_contribution", 6),
			#(val_div, ":freelancer_player_contribution", 5), #level * 1.2 (for a bit of a scaling bump)
			#(val_max, ":freelancer_player_contribution", 10), #and to give a base line
			#(assign, "$g_strength_contribution_of_player", ":freelancer_player_contribution"),
				(else_try),
			#Caba freelancer fixes end
					(gt, "$g_starting_strength_friends", 0), #this new to prevent occasional div by zero error
					(val_div, "$g_strength_contribution_of_player","$g_starting_strength_friends"),
				(else_try),
					(assign, "$g_strength_contribution_of_player", 100), #Or zero, maybe
				(try_end),
				
				(party_clear, "p_routed_enemies"), #new
				(assign, "$num_routed_us", 0),#newtoday
				(assign, "$num_routed_allies", 0),#newtoday
				(assign, "$num_routed_enemies", 0),#newtoday
				(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
				(try_for_range, ":i_stack", 0, ":num_stacks"),
					(party_stack_get_troop_id, ":stack_troop_id", "p_main_party", ":i_stack"),
					(try_begin),
						(troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
						#(troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
						#(troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
					(try_end),
				(try_end),
				
				(party_get_num_companion_stacks, ":num_stacks", "p_collective_friends"),
				(try_for_range, ":i_stack", 0, ":num_stacks"),
					(party_stack_get_troop_id, ":stack_troop_id", "p_collective_friends", ":i_stack"),
					(try_begin),
						#(troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
						#(troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
						(troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
					(try_end),
				(try_end),
				
				(party_get_num_companion_stacks, ":num_stacks", "p_collective_enemy"),
				(try_for_range, ":i_stack", 0, ":num_stacks"),
					(party_stack_get_troop_id, ":stack_troop_id", "p_collective_enemy", ":i_stack"),
					(try_begin),
						#(troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
						(troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
						#(troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
					(try_end),
				(try_end),
				
				(try_for_range, ":cur_faction", fac_kingdom_1, fac_kingdoms_end),
					(faction_set_slot, ":cur_faction", slot_faction_num_routed_agents, 0),
				(try_end),
				
				(assign, "$routed_party_added", 0), #new
				(party_clear, "p_total_enemy_casualties"), #new
				
				#      (try_begin),
				#        (gt, "$g_ally_party", 0),
				#        (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
				#        (call_script, "script_party_calculate_strength", "p_collective_ally"),
				#        (assign, "$g_starting_strength_ally_party", reg0),
				#        (store_add, ":starting_strength_factor_combined","$g_starting_strength_ally_party","$g_starting_strength_main_party"),
				#         (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 80), #reduce contribution if we are helping someone.
				#        (val_div, "$g_strength_contribution_of_player",":starting_strength_factor_combined"),
				#      (try_end),
		])
		
