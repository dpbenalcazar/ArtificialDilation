%% Manual segmentation of iris images
%
% This program will show you all the images in a folder
% Click with the mouse 4 points in the pupil/iris boundary and then click 
% 4 points in the iris/sclera boundary
% Therefore you must click 8 consecutive times per image
%
% Created by: Daniel Benalcazar
% Year of first version: 2018
% Last update: 2022

%% I/O files and folders

folder = '..\samples\';
csv_file = '..\samples\segm.csv';

Files = dir([folder,'*.png']);
Nf = length(Files);

%% Read Previous Segmentation

last = num2str(Nf+1);
fields = {'ID','x_pup','y_pup','r_pup','x_iri','y_iri','r_iri'};
IDs = {Files.name}';

if exist(csv_file, 'file')
    cir_pupi = xlsread(csv_file, 1, ['B2:D',last]);
    cir_iris = xlsread(csv_file, 1, ['E2:G',last]);
else
    cir_pupi = zeros(Nf,3);
    cir_iris = zeros(Nf,3);
end

%% Label Pupil and Iris

for f = 1:Nf % alternatively place list of files to modify, i.e.: [1:2,4]
    % Read input image:
    name = [folder, Files(f).name];    
    img1 = imread(name);
    
    % Show image
    img_title = forTitle([Files(f).name]);
    figure(1);
    imshow(img1);
    colormap(jet(256));
    title(img_title)
    drawnow;
    
    % Get clicked positions
    [X,Y] = ginput(8);
    
    % Find best-fitting circles
    [xp, yp, Rp] = circfit(X(1:4),Y(1:4));   
    [xi, yi, Ri] = circfit(X(5:8),Y(5:8));
    
    
    % Store segmentation data
    cir_pupi(f,:) = [xp, yp, Rp];
    cir_iris(f,:) = [xi, yi, Ri];
    IDs{f} = Files(f).name;
    
    % Draw found circles
    img2 = insertShape(img1,'circle',[xp, yp, Rp],'LineWidth',5,'Color','blue');
    img2 = insertShape(img2,'circle',[xi, yi, Ri],'LineWidth',5,'Color','red');
    
    % Show segmented image
    figure(2);
    imshow(img2);
    img_title(img_title)
    drawnow;
end


%% Save segmentation

data = [cir_pupi, cir_iris];

xlswrite(csv_file, fields, 1);
xlswrite(csv_file, IDs,  1, 'A2');
xlswrite(csv_file, data, 1, 'B2');
