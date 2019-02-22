import * as React from 'react';
import { FastLayer, Rect } from 'react-konva';
import * as _ from 'underscore';
import {colors} from './Constants';
import {IPawnGoalPosition} from './IVisualization';

export interface IBoardProps {
    numberOfTile: number;
    size: number;
    gap: number;
    goals: IPawnGoalPosition[]
}

export class Board extends React.Component<IBoardProps> {
    public render() {
        const {numberOfTile, size, gap} = this.props;

        const rects = _.map(_.range(numberOfTile), (y: number) => {
            const posY = y * size + y * gap;
            return _.map(_.range(numberOfTile), (x: number) => {
                const posX = x * size + x * gap;
                return (
                    <React.Fragment key={`rect-${x}-${y}`}>
                        <Rect
                            key='background'
                            fill="#444"
                            opacity={0.4}
                            width={size}
                            height={size}
                            x={posX}
                            y={posY}
                        />
                        <Rect
                            key='border'
                            fill="transparent"
                            opacity={0.4}
                            width={size}
                            height={size}
                            x={posX}
                            y={posY}
                            stroke='#4FC6F4'
                            strokeWidth={0.5}
                            shadowColor='#4FC6F4'
                            shadowBlur={5}
                        />
                    </React.Fragment>
                );
            });
        });
        const goals = this.props.goals.map((g: IPawnGoalPosition, i: number) => {
            const [y, x] = g['py/tuple'];
            const length = (size - 1) * numberOfTile + (gap - 1) * numberOfTile;
            const commonProps = {
                fill: 'transparent',
                key: `goal-${i}`,
                opacity: 0.2,
                shadowBlur: 10,
                shadowColor: colors[i],
                stroke: colors[i],
                strokeWidth: 1,
            };
            if (y !== null) {
                return (
                    <Rect
                        width={length}
                        height={1}
                        x={0}
                        y={y > 0 ? y * size + (y - 0.5) * gap : size + 0.5 * gap}
                        {...commonProps}
                    />
                )
            } else if (x !== null) {
                return (
                    <Rect
                        width={1}
                        height={length}
                        x={x > 0 ? x * size + (x - 0.5) * gap : size + 0.5 * gap}
                        y={0}
                        {...commonProps}
                    />
                );
            }
            return null;
        });
        return (
            <FastLayer>{rects}{goals}</FastLayer>
        );
    }
}
