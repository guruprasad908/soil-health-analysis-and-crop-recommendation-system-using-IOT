// FarmCanvas.jsx
// React-Konva component for rendering the farm layout

import React, { useRef, useEffect, useState } from 'react';
import { Stage, Layer, Image, Rect, Text, Group } from 'react-konva';
import { getCropTexturePath, preloadImage } from '../utils/textureLoader';

// Fallback soil texture path
const SOIL_TEXTURE_PATH = '/src/assets/textures/soil.png';

/**
 * FarmCanvas component to render the mixed cropping layout
 * @param {object} layout - Layout data from API
 * @param {number} containerWidth - Width of the container
 * @param {number} containerHeight - Height of the container
 */
const FarmCanvas = ({ layout, mixedCrops, containerWidth, containerHeight }) => {
  const stageRef = useRef();
  const [soilPattern, setSoilPattern] = useState(null);
  const [cropTextures, setCropTextures] = useState({});
  const [hoveredSection, setHoveredSection] = useState(null);

  // Calculate scale to fit container while maintaining aspect ratio
  const scale = layout && layout.width && layout.height ? Math.min(
    containerWidth / layout.width,
    containerHeight / layout.height
  ) : 1;

  const scaledWidth = layout && layout.width ? layout.width * scale : containerWidth;
  const scaledHeight = layout && layout.height ? layout.height * scale : containerHeight;

  // Load soil texture
  useEffect(() => {
    const loadSoilTexture = async () => {
      try {
        const img = await preloadImage(SOIL_TEXTURE_PATH);
        const pattern = img;
        setSoilPattern(pattern);
      } catch (error) {
        console.warn('Failed to load soil texture:', error);
      }
    };

    loadSoilTexture();
  }, []);

  // Load crop textures
  useEffect(() => {
    const loadCropTextures = async () => {
      const textures = {};
      const texturePromises = layout.sections.map(async (section) => {
        try {
          const texturePath = await getCropTexturePath(section.crop);
          const img = await preloadImage(texturePath);
          textures[section.crop] = img;
        } catch (error) {
          console.warn(`Failed to load texture for ${section.crop}:`, error);
        }
      });

      await Promise.all(texturePromises);
      setCropTextures(textures);
    };

    if (layout && layout.sections) {
      loadCropTextures();
    }
  }, [layout, mixedCrops]);

  // Handle section hover
  const handleSectionMouseEnter = (section) => {
    setHoveredSection(section);
  };

  const handleSectionMouseLeave = () => {
    setHoveredSection(null);
  };

  if (!layout || !layout.sections) {
    return <div className="farm-canvas-placeholder">No layout data available</div>;
  }

  return (
    <div className="farm-canvas-container">
      <Stage
        ref={stageRef}
        width={scaledWidth}
        height={scaledHeight}
        scaleX={scale}
        scaleY={scale}
        className="farm-stage"
      >
        {/* Background Layer */}
        <Layer>
          {soilPattern && (
            <Rect
              x={0}
              y={0}
              width={layout.width}
              height={layout.height}
              fillPatternImage={soilPattern}
              fillPatternRepeat="repeat"
            />
          )}
        </Layer>

        {/* Crop Sections Layer */}
        <Layer>
          {layout.sections.map((section, index) => {
            // Apply padding between sections
            const padding = 10;
            const x = section.x + (index === 0 ? 0 : padding / 2);
            const y = section.y + (index === 0 ? 0 : padding / 2);
            const w = section.w - padding;
            const h = section.h - padding;

            // Find area percentage for this crop
            const cropInfo = mixedCrops?.find(c => c.crop === section.crop);
            const areaPercent = cropInfo ? cropInfo.area_percent : 0;

            return (
              <Group key={`${section.crop}-${index}`}>
                {/* Crop Texture */}
                {cropTextures[section.crop] && (
                  <Image
                    x={x}
                    y={y}
                    width={w}
                    height={h}
                    image={cropTextures[section.crop]}
                    onMouseEnter={() => handleSectionMouseEnter(section)}
                    onMouseLeave={handleSectionMouseLeave}
                  />
                )}

                {/* Section Border */}
                <Rect
                  x={x}
                  y={y}
                  width={w}
                  height={h}
                  stroke="rgba(0, 0, 0, 0.7)"
                  strokeWidth={2}
                  shadowColor="black"
                  shadowBlur={5}
                  shadowOpacity={0.3}
                  shadowOffsetX={2}
                  shadowOffsetY={2}
                  onMouseEnter={() => handleSectionMouseEnter(section)}
                  onMouseLeave={handleSectionMouseLeave}
                />

                {/* Crop Label */}
                <Text
                  x={x + w / 2}
                  y={y + h / 2}
                  text={`${section.crop}\n${areaPercent}%`}
                  fontSize={16}
                  fontStyle="bold"
                  fill="white"
                  shadowColor="black"
                  shadowBlur={3}
                  shadowOpacity={0.8}
                  shadowOffsetX={1}
                  shadowOffsetY={1}
                  align="center"
                  verticalAlign="middle"
                  width={w}
                  height={h}
                />
              </Group>
            );
          })}
        </Layer>

        {/* Tooltip Layer */}
        {hoveredSection && (
          <Layer>
            <Rect
              x={hoveredSection.x + 10}
              y={hoveredSection.y + 10}
              width={150}
              height={60}
              fill="rgba(0, 0, 0, 0.8)"
              cornerRadius={5}
            />
            <Text
              x={hoveredSection.x + 20}
              y={hoveredSection.y + 20}
              text={`${hoveredSection.crop}\nArea: ${hoveredSection.w} x ${hoveredSection.h}m`}
              fontSize={12}
              fill="white"
              fontStyle="bold"
            />
          </Layer>
        )}
      </Stage>
    </div>
  );
};

export default FarmCanvas;