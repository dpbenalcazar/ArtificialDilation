function txt2 = forTitle(txt1)
% Eliminates dashes from text to avoid showing characters as subindexes

    ind = txt1=='_';
    txt1(ind) = ' ';
    txt2 = txt1;
    
end

