function im2 = change_dilation_v2(im1, dil, pupil_xyr, iris_xyr)
% Changes the dilation level in the input image im1 to the one specified by
% the variable dil [0, 1].
% Inputs pupil_xyr and iris_xyr are the circular segmentation of the iris
% image in the format: [x, y, r]
%
% This version uses masks to identify pixels that belong to the pupil and
% the iris, reducing processing time in 33%. 
    
    % Original pupuil and iris radii:
    rp1 = pupil_xyr(3);
    ri = iris_xyr(3);
    
    % Output pupil radius:
    rp2 = dil*ri;
    
    % Slope for lineal transformation:
    m = (ri-rp1)/(ri-rp2);
    
    % Output image:
    [N,M,~] = size(im1);
    
    % Find new pupil and iris masks
    xp = pupil_xyr(1);
    yp = pupil_xyr(2);
    rp = 0.97*rp2;
    bgm = zeros(N,M,3,'uint8');
    pupil_mask = insertShape(bgm, 'FilledCircle', [xp, yp, rp], 'color', 'white', 'opacity', 1);
    iris_mask  = insertShape(bgm, 'FilledCircle', [xp, yp, ri], 'color', 'white', 'opacity', 1);
    pupil_mask = pupil_mask(:,:,1) > 0;
    iris_mask  =  iris_mask(:,:,1) > 0;
    iris_mask(pupil_mask) = 0;
    
    % Create output image
    im2 = im1;
    
    % Sample new iris
    [v, u] = find(iris_mask);
    xp = u - pupil_xyr(1);
    yp = v - pupil_xyr(2);
    rp = sqrt(xp.^2 + yp.^2);
    th = atan2(yp, xp);
    r = m*(rp-rp2)+rp1;
    x = round(r.*cos(th) + pupil_xyr(1));
    y = round(r.*sin(th) + pupil_xyr(2));
    im2(v,u,:) = im1(y,x,:);
    
    % Sample new pupil
    [v, u] = find(pupil_mask);
    xp = u - pupil_xyr(1);
    yp = v - pupil_xyr(2);
    rp = sqrt(xp.^2+yp.^2);
    r = rp1*rp/rp2;
    th = atan2(yp,xp);
    x = round(r.*cos(th) + pupil_xyr(1));
    y = round(r.*sin(th) + pupil_xyr(2));
    im2(v,u,:) = im1(y,x,:);
    
end