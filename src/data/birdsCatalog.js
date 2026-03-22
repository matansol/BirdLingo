import quizTiersData from '../../data/quiz_tiers_data.json';
import birdImages from '../../assets/birdImages';

export const allBirdEntities = Object.values(quizTiersData.entities || {});

export const tierIds = {
  1: new Set(quizTiersData.tiers?.['1'] || []),
  2: new Set(quizTiersData.tiers?.['2'] || []),
  3: new Set(quizTiersData.tiers?.['3'] || []),
};

const availableImageFiles = new Set(
  Object.values(birdImages).flat().map((fileName) => String(fileName))
);

// Filter out birds that don't have a matching image file
export const birdsWithImages = allBirdEntities.filter((bird) => {
  const imageKey = bird.image ? bird.image.replace(/_\d+$/, '') : null;
  const hasImageByKey = imageKey && birdImages[imageKey];
  const hasImageByFileName = Array.isArray(bird.images)
    && bird.images.some((fileName) => availableImageFiles.has(String(fileName)));
  return hasImageByKey || hasImageByFileName;
});

export const birdById = {};
birdsWithImages.forEach((bird) => {
  birdById[bird.id] = bird;
});

export const getTierBirds = (tier) => {
  const tierSet = tierIds[tier] || new Set();
  return birdsWithImages.filter((bird) => tierSet.has(bird.id));
};

export const getTierBirdIds = (tier) => getTierBirds(tier).map((bird) => bird.id);
