import * as React from 'react';
import * as _ from 'underscore';
import {FastLayer, Rect} from 'react-konva';
import {blurSize, Wall} from './Constants';

export interface WallsProps {
    size: number;
    gap: number;
    horizontal: Wall[];
    vertical: Wall[];
}

export class Walls extends React.Component<WallsProps> {
    render() {
        const {gap, size, horizontal, vertical} = this.props;
        const wallSize = 0.2 * gap;

        const horizontalWalls = _.map(horizontal, (wall: Wall, i: number) => {
            const [y, x] = wall.position;
            const posY = (y + 1) * size + y * gap + (2 * wallSize);
            const posX = x * size + x * gap - (0.5 * gap) - (wallSize / 2);
            return (
                <Rect
                    key={`horizontal-${i}`}
                    width={2 * size + 2 * gap + wallSize + Math.min(0, posX)}
                    height={wallSize}
                    y={posY}
                    x={Math.max(0, posX)}
                    fill={wall.color}
                    shadowBlur={blurSize}
                    shadowColor={wall.color}
                />
            );
        });
        const verticalWalls = _.map(vertical, (wall: Wall, i: number) => {
            const [y, x] = wall.position;
            const posY = y * size + y * gap - (0.5 * gap) - (wallSize / 2);
            const posX = (x + 1) * size + x * gap + (2 * wallSize);
            return (
                <Rect
                    key={`vertical-${i}`}
                    height={2 * size + 2 * gap + wallSize + Math.min(0, posY)}
                    width={wallSize}
                    y={Math.max(0, posY)}
                    x={posX}
                    fill={wall.color}
                    shadowBlur={blurSize}
                    shadowColor={wall.color}
                />
            );
        });
        return (
            <FastLayer>
                {horizontalWalls}
                {verticalWalls}
            </FastLayer>
        );
    }
}
