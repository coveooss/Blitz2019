import * as React from 'react';
import { Path, Line } from 'react-konva';
import { PlayerIcon } from './Icons';

export interface IPlayerProps {
    color: string;
    size: number;
    x: number;
    y: number;
    isDead: boolean;
}

interface CommonProps {
    data: string;
    x: number;
    y: number;
    scaleX: number;
    scaleY: number;
}

export class Player extends React.Component<IPlayerProps> {
    public render() {
        const basicSize = 38;
        const scale = this.props.size / basicSize;
        const sizeRatio = 0.75;
        const offset = basicSize * scale * sizeRatio / 4;
        const commonProps: CommonProps = {
            data: PlayerIcon,
            x: this.props.x + offset,
            y: this.props.y + offset,
            scaleX: scale * sizeRatio,
            scaleY: scale * sizeRatio,
        };
        return (
            <React.Fragment key={`player-${this.props.color}`}>
                <Path
                    key='background'
                    fill={this.props.color}
                    opacity={this.props.isDead ? 0.2 : 0.3}
                    {...commonProps}
                />
                <Path
                    key='frontground'
                    fill='transparent'
                    stroke={this.props.color}
                    strokeWidth={4}
                    shadowBlur={5}
                    shadowColor={this.props.color}
                    shadowOpacity={1}
                    opacity={this.props.isDead ? 0.5 : 1}
                    {...commonProps}
                />
                {this.props.isDead && <>
                    <Line
                        key='dead-left'
                        x={commonProps.x}
                        y={commonProps.y}
                        scaleX={commonProps.scaleX}
                        scaleY={commonProps.scaleY}
                        points={[0, 0, 38 * 0.9, 38 * 0.9]}
                        stroke={this.props.color}
                        strokeWidth={3}
                        opacity={1}
                    />
                    <Line
                        key='dead-right'
                        x={commonProps.x}
                        y={commonProps.y}
                        scaleX={-commonProps.scaleX}
                        scaleY={commonProps.scaleY}
                        points={[-38 * 0.9, 0, 0, 38 * 0.9]}
                        stroke={this.props.color}
                        strokeWidth={3}
                        opacity={1}
                    />
                </>}
            </React.Fragment>
        );
    }
}
