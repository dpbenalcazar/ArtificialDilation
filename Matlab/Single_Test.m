im1 = im2double(imread('../samples/LVL.png'));

pupil_xyr = [200, 200, 51];
iris_xyr = [196, 210, 181];

% Original Dilation Ratio (Rp/Ri):
dil1 = pupil_xyr(3)/iris_xyr(3);

% Dilation ratios of images 2 and 3:
dil2 = 0.15;
dil3 = 0.5;

% Change Dilation
tic
im2 = change_dilation(im1, dil2, pupil_xyr, iris_xyr);
im3 = change_dilation(im1, dil3, pupil_xyr, iris_xyr);
toc

figure(1)
subplot 131
imshow(im1)
title('Original')
xlabel(['Rp/Ri = ',num2str(dil1,'%0.3f')])

subplot 132
imshow(im2)
title('Reduced Dilation')
xlabel(['Rp/Ri = ',num2str(dil2,'%0.3f')])

subplot 133
imshow(im3)
title('Increased Dilation')
xlabel(['Rp/Ri = ',num2str(dil3,'%0.3f')])
