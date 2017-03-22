screenfile = 'screendata.csv';
touchfile = 'touchdata.csv';

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

figure;
plot(timetouch,touchdelay);

%smoothing of time vector???
%determine best way

timetouchnew = smooth(timetouch,10000,'moving');
timetouchnew2 = medfilt1(timetouch,1000);


%% CREATE BOOLEAN VECTOR FOR PHONE USAGE

%assuming linear time vector
phone_in_use = zeros(length(timetouch),1);

for ii = 1:length(timetouch)
    if touchdelay(ii) < 60 % && screenon(ii) % touch within one minute means phone is in use, unless screen goes black??
        phone_in_use(ii) = 1;
    end
end


