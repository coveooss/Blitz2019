import * as React from 'react';
import { Layer } from 'react-konva';
import { shallow } from 'enzyme';
import { Board } from './Board';

test('Basic test', () => {
    const width: number = 400;
    const numberOfTile: number = 9;
    const tileSize = width / numberOfTile;

    const board = shallow(<Board numberOfTile={numberOfTile} gap={tileSize * 0.2} size={tileSize * 0.8} />);

    expect(board.find(Layer)).toBeDefined();
});