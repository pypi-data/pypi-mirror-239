
function initialize(box)

	dofile("C:/Users/arthur.desbois/Documents/dev/openvibeScripting/openvibe-automation/BraccioScenar/lua-stimulator-stim-codes.lua")

	number_of_trials = box:get_setting(2)
	first_class = _G[box:get_setting(3)]
	second_class = _G[box:get_setting(4)]
	baseline_duration = box:get_setting(5)
	wait_for_beep_duration = box:get_setting(6)
	wait_for_cue_duration = box:get_setting(7)
	display_cue_duration = box:get_setting(8)
	feedback_duration = box:get_setting(9)
	end_of_trial_min_duration = box:get_setting(10)
	end_of_trial_max_duration = box:get_setting(11)
	ErrorRelatedpotential_duration = box:get_setting(12)
	First_ClassError = _G[box:get_setting(13)]
    Second_ClassError = _G[box:get_setting(14)]

	-- initializes random seed
	math.randomseed(os.time())

	repeat
	-- fill the sequence table with predifined order
		sequence = {}
		for i = 1, number_of_trials do
			table.insert(sequence, 1, first_class)
			table.insert(sequence, 1, second_class)
		end

	
	
		-- randomize the sequence
		for i = 1, number_of_trials do
			a = math.random(1, number_of_trials*2)
			b = math.random(1, number_of_trials*2)
			swap = sequence[a]
			sequence[a] = sequence[b]
			sequence[b] = swap
		end
		flag = 0
		for i = 3,number_of_trials*2 do
			if sequence[i-1] == sequence[i] then
				if sequence[i-2] == sequence[i] then
					flag = 1
				end
			end
		end

	until( flag == 0)
	sequence_error = {}
	for i = 1, number_of_trials do
		table.insert(sequence_error, 1, First_ClassError)
		table.insert(sequence_error, 1, Second_ClassError)
	end

	
	-- randomize the sequence
	for i = 1, number_of_trials do
		a = math.random(1, number_of_trials*2)
		b = math.random(1, number_of_trials*2)
		swap = sequence_error[a]
		sequence_error[a] = sequence_error[b]
		sequence_error[b] = swap
	end

end

function process(box)

	local t=0

	-- manages baseline

	box:send_stimulation(1, OVTK_StimulationId_ExperimentStart, t, 0)
	t = t + 5

	box:send_stimulation(1, OVTK_StimulationId_BaselineStart, t, 0)
	box:send_stimulation(1, OVTK_StimulationId_Beep, t, 0)
	t = t + baseline_duration

	box:send_stimulation(1, OVTK_StimulationId_BaselineStop, t, 0)
	box:send_stimulation(1, OVTK_StimulationId_Beep, t, 0)
	t = t + 5

	-- manages trials

	for i = 1, number_of_trials*2 do

		-- first display cross on screen

		box:send_stimulation(1, OVTK_GDF_Start_Of_Trial, t, 0)
		box:send_stimulation(1, OVTK_GDF_Cross_On_Screen, t, 0)
		t = t + wait_for_beep_duration

		-- warn the user the cue is going to appear

		box:send_stimulation(1, OVTK_StimulationId_Beep, t, 0)
		t = t + wait_for_cue_duration

		-- display cue

		box:send_stimulation(1, sequence[i], t, 0)
		
		t = t + display_cue_duration

		-- provide feedback

		box:send_stimulation(1, OVTK_GDF_Feedback_Continuous, t, 0)
		t = t + feedback_duration
		box:send_stimulation(1,OVTK_StimulationId_VisualStimulationStart, t, 0)
		box:send_stimulation(1,sequence_error[i],t,0)
		-- ends trial
		t = t + ErrorRelatedpotential_duration
		box:send_stimulation(1, OVTK_GDF_End_Of_Trial, t, 0)
		t = t + math.random(end_of_trial_min_duration, end_of_trial_max_duration)

	end

	-- send end for completeness
	box:send_stimulation(1, OVTK_GDF_End_Of_Session, t, 0)
	t = t + 5

	box:send_stimulation(1, OVTK_StimulationId_Train, t, 0)
	t = t + 1
	
	-- used to cause the acquisition scenario to stop
	box:send_stimulation(1, OVTK_StimulationId_ExperimentStop, t, 0)

end
