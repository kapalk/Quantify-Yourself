screenfile = 'screenon.csv';
touchfile = 'touchevents.csv';

screendata = csvread(screenfile,1,0);
touchdata = csvread(touchfile,1,0);

%%
% Convert time vectors to matlab datenum
timetouch = datenum(touchdata(:,1)/86400 + datenum('1970-01-01','yyyy-mm-dd')); 
timescreen = datenum(screendata(:,1)/86400 + datenum('1970-01-01','yyyy-mm-dd'));

touchcount = touchdata(:,2);       % number of touches since last datapoint
touchdelay = touchdata(:,3);  
touchdelay = touchdelay / 1000;    % get touch delay in seconds 

screenon = screendata(:,2);        % boolean vector of times when screen on

%%

%figure;
%plot(timetouch,touchdelay);

%smoothing of time vector???
%determine best way

timetouchnew = smooth(timetouch,10000,'moving');
timetouchnew2 = medfilt1(timetouch,1000);


%% CREATE BOOLEAN VECTOR FOR PHONE USAGE

%assuming linear time vector
phone_in_use = zeros(length(timetouch),1);
delays = []; % delay threshold used
nPeriodsList = []; % number of periods
periodLengthList = []; % lengths of periods
for delay = 10:1000
    for ii = 1:length(timetouch)
        if touchdelay(ii) < delay
            phone_in_use(ii) = 1;
        end
    end
    nPeriods = 0;
    jj = 1;
    periodLengths = [];
    while jj < length(phone_in_use)
        if phone_in_use(jj)
            periodLength = 1;
            nPeriods = nPeriods + 1;
            while phone_in_use(jj)
                periodLength = periodLength + 1;
                jj = jj + 1;
            end
            periodLengths(end+1) = periodLength;
        else
            jj = jj + 1;
        end
    end
    periodLengthList(end+1) = mean(periodLengths);
    delays(end+1) = delay;
    nPeriodsList(end+1) = nPeriods;
    fprintf('Number of periods with delay %d was %d.\n',delay,nPeriods);
end

figure;
plot(delays, nPeriodsList);
%figure

%figure;
%stairs(phone_in_use);

