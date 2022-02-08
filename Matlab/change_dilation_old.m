function im2 = change_dilation_old(im1, dil, pupil_xyr, iris_xyr)
% Changes the dilation level in the input image im1 to the one specified by
% the variable dil [0, 1].
% Inputs pupil_xyr and iris_xyr are the circular segmentation of the iris
% image in the format: [x, y, r]
%
% This version tests the distance of each pixel with respect to the pupil
% center to identify pixels that belong to the pupil and the iris.
    
    % Color of the central pixel:
    if size(im1,3) == 3
        Rpup = im1(int32(pupil_xyr(1)), int32(pupil_xyr(2)) ,1);
        Gpup = im1(int32(pupil_xyr(1)), int32(pupil_xyr(2)) ,2);
        Bpup = im1(int32(pupil_xyr(1)), int32(pupil_xyr(2)) ,3);
        col = [Rpup Gpup Bpup];
    else
        col = im1(int32(pupil_xyr(1)), int32(pupil_xyr(2)));
    end
    
    % Original pupuil and iris radii:
    rp1 = pupil_xyr(3);
    ri = iris_xyr(3);
    
    % Output pupil radius:
    rp2 = dil*ri;
    
    % Slope for lineal transformation:
    m = (ri-rp1)/(ri-rp2);
    
    % Output image:
    [N,M,~] = size(im1);
    im2 = zeros(size(im1));
    
    % Change dlation level
    for u = 1:M
        for v = 1:N
            % Get center and radius
            xp = u - pupil_xyr(1);
            yp = v - pupil_xyr(2);
            r_aux = xp^2+yp^2;
            
            % Check if current point is inside the iris
            if r_aux <= ri^2 && r_aux >= rp2^2
                % Find coordinates to sample original image
                rp = sqrt(r_aux);
                th = atan2(yp,xp);
                r = m*(rp-rp2)+rp1;
                x = round(r*cos(th) + pupil_xyr(1));
                y = round(r*sin(th) + pupil_xyr(2));
            
            % Check if current point is inside the pupil
            elseif r_aux < rp2^2
                % Find coordinates to sample original image
                rp = sqrt(r_aux);
                th = atan2(yp,xp);
                r = rp1*rp/rp2;
                x = round(r*cos(th) + pupil_xyr(1));
                y = round(r*sin(th) + pupil_xyr(2));
                
            % Check if current point is outside the iris
            else
                x = u;
                y = v;
                r = 2;
            end 
            
            % Sample original image
            if r>0
                im2(v,u,:) = im1(y,x,:);
            else
                im2(v,u,:) = col;
            end
        end
    end
end

